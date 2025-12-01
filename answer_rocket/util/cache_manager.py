from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path, List

import hashlib
import json
import shutil
from types import FunctionType

import pickle

import sgqlc.types as sgqlc_types
from sgqlc.operation import SelectionList, Selection, Fragment, InlineFragmentSelectionList


class CacheManagerInterface(ABC):
    """Abstract interface for type-specific cache managers."""
    
    @abstractmethod
    def can_handle(self, data: Any) -> bool:
        """Return True if this manager can handle the given data type.
        
        Args:
            data: The data object to check
            
        Returns:
            bool: True if this manager can serialize/deserialize this data type
        """
        pass
    
    @abstractmethod
    def save(self, cache_file: Path, data: Any, qualname: str) -> None:
        """Save data to cache file.
        
        Args:
            cache_file: Base path for cache file (without extension)
            data: The data object to save
            qualname: Qualified name of the cached function for logging
        """
        pass
    
    @abstractmethod
    def load(self, cache_file: Path, qualname: str) -> Any:
        """Load data from cache file.
        
        Args:
            cache_file: Base path for cache file (without extension)
            qualname: Qualified name of the cached function for logging
            
        Returns:
            Any: The deserialized data object
        """
        pass
    
    @abstractmethod
    def get_file_extension(self) -> str:
        """Return the file extension this manager uses.
        
        Returns:
            str: File extension including the dot (e.g. '.pkl', '.json')
        """
        pass


class TestHarnessCacheManager:
    """Coordinator class that manages type-specific cache managers for TestHarness.
    
    This class handles cache file path generation, cache key generation, and 
    delegates serialization/deserialization to appropriate type-specific managers.
    """
    
    def __init__(self, base_cache_dir: Path = None):
        """Initialize the cache manager with type-specific managers.
        
        Args:
            base_cache_dir: Base directory for cache files. Defaults to cache/ in project root.
        """
        if base_cache_dir is None:
            base_cache_dir = Path.cwd() / "cache"
        self.base_cache_dir = base_cache_dir
        
        # Register cache managers in priority order
        # SgqlcCacheManager must be first to handle sgqlc types before they fall to pickle
        self.cache_managers: List[CacheManagerInterface] = [
            SgqlcCacheManager(),
            PickleCacheManager()  # Fallback - must be last
        ]
        
        # Store cache key mapping for debugging - maps hash -> readable data
        self.cache_key_registry = {}
        self._load_cache_key_registry()
    
    def _get_cache_file(self, qualname: str, cache_key: str, save: bool = False) -> Path:
        """Get cache file path for the given qualname and cache_key.
        
        Args:
            qualname: The qualified name of the cached function
            cache_key: The cache key for this specific call
            save: If True, create directories as needed
            
        Returns:
            Path object for the cache file location (without extension)
        """
        # Split qualname by '.' to get all parts
        parts = qualname.split('.')
        
        if len(parts) >= 2:
            # Create directory path from all parts except the last one
            # e.g., "A.A.A" -> cache/A/A/ (directory) and A.pkl (file)
            directory_parts = parts[:-1]  # All parts except the last
            filename = parts[-1]  # Last part becomes the filename
            
            # Create cache directory structure: cache/part1/part2/.../
            cache_dir = self.base_cache_dir / Path(*directory_parts)
            if save:
                cache_dir.mkdir(parents=True, exist_ok=True)
            
            # Return file path at cache/part1/part2/.../filename
            cache_file = cache_dir / f'{filename}_{cache_key}'
        else:
            # Fallback for simple qualnames without structure
            cache_dir = self.base_cache_dir
            if save:
                cache_dir.mkdir(exist_ok=True)
            
            filename = qualname  # Use the entire qualname as filename for simple cases
            cache_file = cache_dir / f'{filename}_{cache_key}'
            
        return cache_file
    
    def get_cache_key(self, method_name: FunctionType, *args, **kwargs) -> str:
        """Generate a stable cache key for method calls and store readable data.
        
        Args:
            method_name: The function being cached
            *args: Positional arguments to the function
            **kwargs: Keyword arguments to the function
            
        Returns:
            str: MD5 hash of the serialized method call
        """
        # Convert args and kwargs to a stable string representation
        def serialize_param(param):
            if isinstance(param, (list, dict)):
                return json.dumps(param, sort_keys=True, default=str)
            return str(param)
        
        cache_data = {
            'method': method_name.__qualname__,
            'args': [serialize_param(arg) for arg in args],
            'kwargs': {k: serialize_param(v) for k, v in sorted(kwargs.items())}
        }
        
        cache_str = json.dumps(cache_data, sort_keys=True)
        cache_key = hashlib.md5(cache_str.encode()).hexdigest()
        
        # Store the readable cache data for debugging
        self.cache_key_registry[cache_key] = cache_data
        self._save_cache_key_registry()
        
        return cache_key
    
    def decode_cache_key(self, cache_key: str) -> dict:
        """Decode a cache key back to its original method call data.
        
        Args:
            cache_key: The MD5 hash cache key
            
        Returns:
            dict: Original cache data with method, args, kwargs or None if not found
        """
        return self.cache_key_registry.get(cache_key)
    
    def get_cache_key_info(self, cache_key: str) -> str:
        """Get human-readable information about a cache key.
        
        Args:
            cache_key: The MD5 hash cache key
            
        Returns:
            str: Formatted string with method call information
        """
        cache_data = self.decode_cache_key(cache_key)
        if cache_data is None:
            return f"Cache key {cache_key} not found in registry"
        
        method = cache_data['method']
        args = cache_data['args']
        kwargs = cache_data['kwargs']
        
        # Format for readability
        args_str = ", ".join(args) if args else ""
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""
        
        params = []
        if args_str:
            params.append(args_str)
        if kwargs_str:
            params.append(kwargs_str)
        
        params_formatted = ", ".join(params)
        
        return f"{method}({params_formatted})"
    
    def _get_registry_file(self) -> Path:
        """Get the path for the cache key registry file."""
        return self.base_cache_dir / "cache_key_registry.json"
    
    def _save_cache_key_registry(self) -> None:
        """Persist the cache key registry to disk."""
        try:
            registry_file = self._get_registry_file()
            registry_file.parent.mkdir(parents=True, exist_ok=True)
            with open(registry_file, 'w') as f:
                json.dump(self.cache_key_registry, f, indent=2)
        except Exception as e:
            # Don't fail cache operations if registry save fails
            print(f"Warning: Could not save cache key registry: {e}")
    
    def _load_cache_key_registry(self) -> None:
        """Load the cache key registry from disk."""
        try:
            registry_file = self._get_registry_file()
            if registry_file.exists():
                with open(registry_file, 'r') as f:
                    self.cache_key_registry = json.load(f)
        except Exception as e:
            # Don't fail initialization if registry load fails
            print(f"Warning: Could not load cache key registry: {e}")
            self.cache_key_registry = {}
    
    def save_cache_data(self, qualname: str, cache_key: str, data: Any) -> None:
        """Save data to cache using the appropriate type-specific manager.
        
        Args:
            qualname: The qualified name of the cached function
            cache_key: The cache key for this specific call
            data: The data to cache
            
        Raises:
            Exception: If no cache manager can handle the data type
        """
        cache_file = self._get_cache_file(qualname, cache_key, save=True)
        
        # Check if already cached
        existing_files = list(cache_file.parent.glob(f'{cache_file.stem}*'))
        if existing_files:
            print(f'{qualname} already in cache at: {existing_files}')
            return
        
        # Find the appropriate cache manager
        for manager in self.cache_managers:
            if manager.can_handle(data):
                try:
                    manager.save(cache_file, data, qualname)
                    return
                except Exception as e:
                    cache_info = self.get_cache_key_info(cache_key)
                    print(f'Failed to save {qualname} with {manager.__class__.__name__}: {e}')
                    print(f'Cache key info: {cache_info}')
                    continue
        
        cache_info = self.get_cache_key_info(cache_key)
        raise Exception(f"No cache manager can handle data type: {type(data)}\nCache key info: {cache_info}")
    
    def load_cache_data(self, qualname: str, cache_key: str) -> Any:
        """Load data from cache using file extension detection.
        
        Args:
            qualname: The qualified name of the cached function
            cache_key: The cache key for this specific call
            
        Returns:
            Any: The loaded data object
            
        Raises:
            Exception: If no cache file is found or loading fails
        """
        cache_file = self._get_cache_file(qualname, cache_key, save=False)
        
        # Try each manager's file extension
        for manager in self.cache_managers:
            extension = manager.get_file_extension()
            candidate_file = cache_file.with_suffix(extension)
            if candidate_file.exists():
                try:
                    return manager.load(cache_file, qualname)
                except Exception as e:
                    cache_info = self.get_cache_key_info(cache_key)
                    print(f'Failed to load {qualname} with {manager.__class__.__name__}: {e}')
                    print(f'Cache key info: {cache_info}')
                    continue
        
        cache_info = self.get_cache_key_info(cache_key)
        raise Exception(f'{qualname} not in cache at {cache_file}\nCache key info: {cache_info}')
    
    def delete_cache(self, force: bool = False) -> None:
        """Delete the entire cache directory and clear registry.
        
        Args:
            force: If True, delete even if some files can't be removed
        """
        if self.base_cache_dir.exists():
            print("Deleting cache")
            try:
                shutil.rmtree(self.base_cache_dir)
            except OSError as e:
                if not force:
                    print(f"Error deleting cache: {e.filename} - {e.strerror}")
                    raise
                else:
                    print(f"Warning: Could not delete {e.filename} - {e.strerror}")
        
        # Clear the in-memory registry
        self.cache_key_registry = {}
    
    def cache_exists(self, qualname: str, cache_key: str) -> bool:
        """Check if a cache file exists for the given qualname and cache_key.
        
        Args:
            qualname: The qualified name of the cached function
            cache_key: The cache key for this specific call
            
        Returns:
            bool: True if any cache file exists for this qualname/cache_key combination
        """
        cache_file = self._get_cache_file(qualname, cache_key, save=False)
        
        # Check if any manager's file extension exists
        for manager in self.cache_managers:
            extension = manager.get_file_extension()
            candidate_file = cache_file.with_suffix(extension)
            if candidate_file.exists():
                return True
        
        return False





class PickleCacheManager(CacheManagerInterface):
    """Fallback cache manager for general objects using pickle format.
    
    This manager should be registered last as it can handle any serializable object.
    """
    
    def can_handle(self, data: Any) -> bool:
        """Check if data can be pickled (fallback for all objects).
        
        Args:
            data: The data object to check
            
        Returns:
            bool: Always True as this is the fallback manager
        """
        return True  # Fallback for everything else
    
    def save(self, cache_file: Path, data: Any, qualname: str) -> None:
        """Save object using pickle format.
        
        Args:
            cache_file: Base path for cache file (without extension)
            data: The object to save
            qualname: Qualified name of the cached function for logging
            
        Raises:
            pickle.PicklingError: If the object cannot be pickled
        """
        pickle_file = cache_file.with_suffix('.pkl')
        try:
            with open(pickle_file, "wb") as f:
                pickle.dump(data, f)
        except pickle.PicklingError as e:
            print(f'{qualname} not picklable: {e}')
            raise e
        except Exception as e:
            print(f'{qualname} not savable: {e}')
            raise e
    
    def load(self, cache_file: Path, qualname: str) -> Any:
        """Load object from pickle file.
        
        Args:
            cache_file: Base path for cache file (without extension)
            qualname: Qualified name of the cached function for logging
            
        Returns:
            Any: The unpickled object
        """
        pickle_file = cache_file.with_suffix('.pkl')
        with open(pickle_file, "rb") as f:
            return pickle.load(f)
    
    def get_file_extension(self) -> str:
        """Return the file extension for pickle files.
        
        Returns:
            str: '.pkl'
        """
        return '.pkl'



class SgqlcCacheManager(CacheManagerInterface):
    """Standalone cache manager for sgqlc objects with fragment support"""
    
    def __init__(self, cache_dir: Path = None):
        """Initialize cache manager with optional cache directory"""
        if cache_dir is None:
            cache_dir = Path(__file__).parent / "cache"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def serialize_selection(self, selection):
        # Only try to access __selection_list__ if it exists (for container types)
        nested_selection_list = None
        if hasattr(selection, '_Selection__selection_list'):
            try:
                nested_selection_list = self._serialize_selection_list(selection._Selection__selection_list)
            except (AttributeError, ValueError):
                # Scalar fields don't have selection lists
                nested_selection_list = None
        
        # Capture fragments and casts that are stored on individual Selection objects
        selection_casts = {}
        selection_fragments = {}
        
        if hasattr(selection, '__casts__') and selection.__casts__:
            selection_casts = {k: self._serialize_cast(v) for k, v in selection.__casts__.items()}
        
        if hasattr(selection, '__fragments__') and selection.__fragments__:
            selection_fragments = {k: [self._serialize_fragment(f) for f in v] for k, v in selection.__fragments__.items()}
        
        return {
            'field_name': selection.__field__.name,
            'field_graphql_name': selection.__field__.graphql_name,
            'alias': selection.__alias__,
            'args': dict(selection.__args__) if selection.__args__ else {},
            'nested_selection_list': nested_selection_list,
            'selection_casts': selection_casts,
            'selection_fragments': selection_fragments
        }

    def _serialize_selection_list(self, selection_list):
        """Serialize a SelectionList to a JSON-serializable format"""
        if selection_list is None:
            return None
        
        return {
            'type_name': selection_list.__type__.__name__,
            'selections': [self.serialize_selection(sel) for sel in selection_list],
            'casts': {k: self._serialize_cast(v) for k, v in selection_list.__casts__.items()},
            'fragments': {k: [self._serialize_fragment(f) for f in v] for k, v in selection_list.__fragments__.items()}
        }

    def _serialize_cast(self, cast_selection_list):
        """Serialize an InlineFragmentSelectionList to a JSON-serializable format"""
        if cast_selection_list is None:
            return None
        
        return {
            'type_name': cast_selection_list.__type__.__name__,
            'selections': [self.serialize_selection(sel) for sel in cast_selection_list],
            'is_inline_fragment': True
        }

    def _serialize_fragment(self, fragment):
        """Serialize a Fragment to a JSON-serializable format"""
        if fragment is None:
            return None
        
        return {
            'name': fragment.__name__,
            'type_name': fragment.__type__.__name__,
            'selections': [self.serialize_selection(sel) for sel in fragment],
            'is_fragment': True
        }

    def _deserialize_selection_list(self, data, schema):
        """Recreate a SelectionList from serialized data"""
        if data is None:
            return None
        
        # Extract base type name from GraphQL type expressions like [Type]! or Type!
        type_name = data['type_name']
        base_type_name = type_name.replace('[', '').replace(']', '').replace('!', '')
        
        # Get the type class from schema using the base type name
        type_class = getattr(schema, base_type_name)
        selection_list = SelectionList(type_class)
        
        # Recreate selections
        for sel_data in data['selections']:
            # Skip special GraphQL introspection fields like __typename
            if sel_data['field_name'].startswith('__') and sel_data['field_name'].endswith('__'):
                continue
                
            # Get the field from the type class using getattr
            field = getattr(type_class, sel_data['field_name'])
            selection = Selection(
                sel_data['alias'],
                field,
                sel_data['args']
            )
            # Recursively recreate nested selection lists
            if sel_data['nested_selection_list']:
                selection._Selection__selection_list = self._deserialize_selection_list(
                    sel_data['nested_selection_list'], schema
                )
            
            # Recreate selection-level casts (inline fragments)
            if 'selection_casts' in sel_data and sel_data['selection_casts']:
                for type_name, cast_data in sel_data['selection_casts'].items():
                    cast_selection_list = self._deserialize_cast(cast_data, schema)
                    selection.__casts__[type_name] = cast_selection_list
            
            # Recreate selection-level fragments (named fragments)
            if 'selection_fragments' in sel_data and sel_data['selection_fragments']:
                for type_name, fragment_list in sel_data['selection_fragments'].items():
                    fragments = []
                    for fragment_data in fragment_list:
                        fragment = self._deserialize_fragment(fragment_data, schema)
                        fragments.append(fragment)
                    selection.__fragments__[type_name] = fragments
            
            selection_list += selection
        
        # Recreate casts (inline fragments)
        for type_name, cast_data in data.get('casts', {}).items():
            cast_selection_list = self._deserialize_cast(cast_data, schema)
            selection_list.__casts__[type_name] = cast_selection_list
        
        # Recreate fragments (named fragments)
        for type_name, fragment_list in data.get('fragments', {}).items():
            fragments = []
            for fragment_data in fragment_list:
                fragment = self._deserialize_fragment(fragment_data, schema)
                fragments.append(fragment)
            selection_list.__fragments__[type_name] = fragments
        
        return selection_list

    def _deserialize_cast(self, data, schema):
        """Recreate an InlineFragmentSelectionList from serialized data"""
        if data is None:
            return None
        
        # Extract base type name from GraphQL type expressions
        base_type_name = data['type_name'].replace('[', '').replace(']', '').replace('!', '')
        type_class = getattr(schema, base_type_name)
        cast_selection_list = InlineFragmentSelectionList(type_class)
        
        # Recreate selections
        for sel_data in data['selections']:
            # Skip special GraphQL introspection fields like __typename
            if sel_data['field_name'].startswith('__') and sel_data['field_name'].endswith('__'):
                continue
                
            field = getattr(type_class, sel_data['field_name'])
            selection = Selection(
                sel_data['alias'],
                field,
                sel_data['args']
            )
            # Recursively recreate nested selection lists
            if sel_data['nested_selection_list']:
                selection._Selection__selection_list = self._deserialize_selection_list(
                    sel_data['nested_selection_list'], schema
                )
            cast_selection_list += selection
        
        return cast_selection_list

    def _deserialize_fragment(self, data, schema):
        """Recreate a Fragment from serialized data"""
        if data is None:
            return None
        
        # Extract base type name from GraphQL type expressions
        base_type_name = data['type_name'].replace('[', '').replace(']', '').replace('!', '')
        type_class = getattr(schema, base_type_name)
        fragment = Fragment(type_class, data['name'])
        
        # Recreate selections
        for sel_data in data['selections']:
            # Skip special GraphQL introspection fields like __typename
            if sel_data['field_name'].startswith('__') and sel_data['field_name'].endswith('__'):
                continue
                
            field = getattr(type_class, sel_data['field_name'])
            selection = Selection(
                sel_data['alias'],
                field,
                sel_data['args']
            )
            # Recursively recreate nested selection lists
            if sel_data['nested_selection_list']:
                selection._Selection__selection_list = self._deserialize_selection_list(
                    sel_data['nested_selection_list'], schema
                )
                    
            fragment += selection
        
        return fragment

    def _recreate_sgqlc_object(self, cached_data, schema):
        """Recreate an sgqlc BaseType object from cached data with proper polymorphic type handling"""
        class_name = cached_data['class_name']
        json_data = cached_data['json_data']
        selection_list_data = cached_data['selection_list']
        
        # Get the class from schema
        class_obj = getattr(schema, class_name)
        
        # Recreate the selection list with improved polymorphic handling and fragment propagation
        selection_list = self._deserialize_selection_list_with_fragment_propagation(selection_list_data, schema)
        
        # Create the object with the original JSON data and recreated selection list
        obj = class_obj(json_data, selection_list)
        
        # Post-process: ensure fragment fields are accessible on nested objects
        self._apply_fragments_to_nested_objects(obj, selection_list, schema)
        
        return obj

    def _apply_fragments_to_nested_objects(self, obj, selection_list, schema):
        """Post-process an object to ensure fragments are applied to nested objects like attributes"""
        if not hasattr(obj, '__dict__') or not selection_list:
            return
            
        # Look for list fields that might contain objects needing fragments
        for attr_name in ['domain_objects', 'attributes']:
            if hasattr(obj, attr_name):
                attr_list = getattr(obj, attr_name, None)
                if attr_list and isinstance(attr_list, list):
                    # Find the selection for this field in the selection list
                    field_selection = None
                    for selection in selection_list:
                        if selection.__field__.name == attr_name:
                            field_selection = selection
                            break
                    
                    if field_selection and hasattr(field_selection, '_Selection__selection_list'):
                        nested_selection_list = field_selection._Selection__selection_list
                        
                        if nested_selection_list and hasattr(nested_selection_list, '__fragments__'):
                            # Apply fragments to each object in the list
                            for item in attr_list:
                                if hasattr(item, '__class__'):
                                    self._apply_fragment_fields_to_object(item, nested_selection_list, schema)
                                    # Recursively apply to nested objects, passing down the fragments
                                    self._apply_fragments_to_nested_objects_with_context(item, nested_selection_list, schema)

    def _apply_fragments_to_nested_objects_with_context(self, obj, parent_selection_list, schema):
        """Apply fragments to nested objects, inheriting fragments from parent context"""
        if not hasattr(obj, '__dict__') or not parent_selection_list:
            return
            
        # Look for list fields that might contain objects needing fragments
        for attr_name in ['attributes']:  # Focus on attributes since domain_objects is handled at top level
            if hasattr(obj, attr_name):
                attr_list = getattr(obj, attr_name, None)
                if attr_list and isinstance(attr_list, list):
                    # Apply inherited fragments to each object in the list
                    for item in attr_list:
                        if hasattr(item, '__class__'):
                            item_type = item.__class__.__name__
                            
                            # Check if we have fragments for this item's type in the parent context
                            if hasattr(parent_selection_list, '__fragments__') and item_type in parent_selection_list.__fragments__:
                                self._apply_fragment_fields_to_object_from_fragments(item, parent_selection_list.__fragments__[item_type], schema)

    def _apply_fragment_fields_to_object_from_fragments(self, obj, fragments, schema):
        """Apply fragment fields to an object directly from fragment definitions"""
        if not fragments:
            return
            
        for fragment in fragments:
            # Apply each field from the fragment to the object
            for selection in fragment:
                field_name = selection.__field__.name
                
                # Skip if object already has this field accessible
                if hasattr(obj, field_name):
                    continue
                    
                # Try to get the value from the object's JSON data
                if hasattr(obj, '__json_data__') and obj.__json_data__:
                    json_data = obj.__json_data__
                    
                    # Convert from GraphQL field name to JSON field name
                    graphql_name = selection.__field__.graphql_name
                    if graphql_name in json_data:
                        # Set the field value directly on the object
                        try:
                            setattr(obj, field_name, json_data[graphql_name])
                        except (AttributeError, TypeError):
                            # Some fields might be read-only, skip them
                            pass

    def _apply_fragment_fields_to_object(self, obj, selection_list, schema):
        """Apply fragment fields to a specific object based on its type"""
        if not hasattr(obj, '__class__') or not selection_list:
            return
            
        obj_type_name = obj.__class__.__name__
        
        # Check if there's a fragment for this object's type
        if hasattr(selection_list, '__fragments__') and obj_type_name in selection_list.__fragments__:
            fragments = selection_list.__fragments__[obj_type_name]
            
            for fragment in fragments:
                # Apply each field from the fragment to the object
                for selection in fragment:
                    field_name = selection.__field__.name
                    
                    # Skip if object already has this field accessible
                    if hasattr(obj, field_name):
                        continue
                        
                    # Try to get the value from the object's JSON data
                    if hasattr(obj, '__json_data__') and obj.__json_data__:
                        json_data = obj.__json_data__
                        
                        # Convert from GraphQL field name to JSON field name
                        graphql_name = selection.__field__.graphql_name
                        if graphql_name in json_data:
                            # Set the field value directly on the object
                            try:
                                setattr(obj, field_name, json_data[graphql_name])
                            except (AttributeError, TypeError):
                                # Some fields might be read-only, skip them
                                pass

    def _deserialize_selection_list_with_types(self, data, schema):
        """Enhanced version that properly handles polymorphic types using __typename from JSON"""
        if data is None:
            return None
        
        # Extract base type name from GraphQL type expressions like [Type]! or Type!
        type_name = data['type_name']
        base_type_name = type_name.replace('[', '').replace(']', '').replace('!', '')
        
        # Get the type class from schema using the base type name
        type_class = getattr(schema, base_type_name)
        selection_list = SelectionList(type_class)
        
        # Recreate selections
        for sel_data in data['selections']:
            # Skip special GraphQL introspection fields like __typename
            if sel_data['field_name'].startswith('__') and sel_data['field_name'].endswith('__'):
                continue
                
            # Get the field from the type class using getattr
            field = getattr(type_class, sel_data['field_name'])
            selection = Selection(
                sel_data['alias'],
                field,
                sel_data['args']
            )
            # Recursively recreate nested selection lists with type awareness
            if sel_data['nested_selection_list']:
                selection._Selection__selection_list = self._deserialize_selection_list_with_types(
                    sel_data['nested_selection_list'], schema
                )
            
            # Recreate selection-level casts (inline fragments)
            if 'selection_casts' in sel_data and sel_data['selection_casts']:
                for type_name, cast_data in sel_data['selection_casts'].items():
                    cast_selection_list = self._deserialize_cast(cast_data, schema)
                    selection.__casts__[type_name] = cast_selection_list
            
            # Recreate selection-level fragments (named fragments)
            if 'selection_fragments' in sel_data and sel_data['selection_fragments']:
                for type_name, fragment_list in sel_data['selection_fragments'].items():
                    fragments = []
                    for fragment_data in fragment_list:
                        fragment = self._deserialize_fragment(fragment_data, schema)
                        fragments.append(fragment)
                    selection.__fragments__[type_name] = fragments
            
            selection_list += selection
        
        # Recreate casts (inline fragments) - these are crucial for polymorphic types
        for type_name, cast_data in data.get('casts', {}).items():
            cast_selection_list = self._deserialize_cast(cast_data, schema)
            selection_list.__casts__[type_name] = cast_selection_list
        
        # Recreate fragments (named fragments) - these define fields for specific types
        for type_name, fragment_list in data.get('fragments', {}).items():
            fragments = []
            for fragment_data in fragment_list:
                fragment = self._deserialize_fragment(fragment_data, schema)
                fragments.append(fragment)
            selection_list.__fragments__[type_name] = fragments
        
        return selection_list

    def _deserialize_selection_list_with_fragment_propagation(self, data, schema, parent_fragments=None):
        """Enhanced version that propagates fragments to nested objects in lists"""
        if data is None:
            return None
        
        # Extract base type name from GraphQL type expressions like [Type]! or Type!
        type_name = data['type_name']
        base_type_name = type_name.replace('[', '').replace(']', '').replace('!', '')
        
        # Get the type class from schema using the base type name
        type_class = getattr(schema, base_type_name)
        selection_list = SelectionList(type_class)
        
        # Get all available fragments - from current level and inherited from parent
        all_fragments = {}
        if parent_fragments:
            all_fragments.update(parent_fragments)
        all_fragments.update(data.get('fragments', {}))
        
        # Recreate selections
        for sel_data in data['selections']:
            # Skip special GraphQL introspection fields like __typename
            if sel_data['field_name'].startswith('__') and sel_data['field_name'].endswith('__'):
                continue
                
            # Get the field from the type class using getattr
            field = getattr(type_class, sel_data['field_name'])
            selection = Selection(
                sel_data['alias'],
                field,
                sel_data['args']
            )
            
            # For nested selection lists, pass down all available fragments
            if sel_data['nested_selection_list']:
                nested_selection_list = self._deserialize_selection_list_with_fragment_propagation(
                    sel_data['nested_selection_list'], schema, all_fragments
                )
                selection._Selection__selection_list = nested_selection_list
                
                # For list fields, ensure the nested selection list includes all relevant fragments
                if sel_data['field_name'] in ['attributes', 'domain_objects']:
                    self._ensure_fragments_for_list_field(nested_selection_list, all_fragments, schema)
            else:
                # Handle the case where attributes field has no nested_selection_list but we have fragments
                if sel_data['field_name'] == 'attributes' and all_fragments:
                    # Create a dynamic selection list for attributes that includes the fragments
                    try:
                        from answer_rocket.graphql.schema import MaxDomainAttribute
                        attr_selection_list = SelectionList(MaxDomainAttribute)
                        
                        # Add all attribute fragments to this selection list
                        self._ensure_fragments_for_list_field(attr_selection_list, all_fragments, schema)
                        
                        # Set this as the selection list for the attributes field
                        selection._Selection__selection_list = attr_selection_list
                    except ImportError:
                        # If we can't import MaxDomainAttribute, continue without optimization
                        pass
            
            # Recreate selection-level casts (inline fragments)
            if 'selection_casts' in sel_data and sel_data['selection_casts']:
                for type_name, cast_data in sel_data['selection_casts'].items():
                    cast_selection_list = self._deserialize_cast(cast_data, schema)
                    selection.__casts__[type_name] = cast_selection_list
            
            # Recreate selection-level fragments (named fragments)
            if 'selection_fragments' in sel_data and sel_data['selection_fragments']:
                for type_name, fragment_list in sel_data['selection_fragments'].items():
                    fragments = []
                    for fragment_data in fragment_list:
                        fragment = self._deserialize_fragment(fragment_data, schema)
                        fragments.append(fragment)
                    selection.__fragments__[type_name] = fragments
            
            selection_list += selection
        
        # Recreate casts (inline fragments) - these are crucial for polymorphic types
        for type_name, cast_data in data.get('casts', {}).items():
            cast_selection_list = self._deserialize_cast(cast_data, schema)
            selection_list.__casts__[type_name] = cast_selection_list
        
        # Recreate fragments (named fragments) - these define fields for specific types
        for type_name, fragment_list in data.get('fragments', {}).items():
            fragments = []
            for fragment_data in fragment_list:
                fragment = self._deserialize_fragment(fragment_data, schema)
                fragments.append(fragment)
            selection_list.__fragments__[type_name] = fragments
        
        return selection_list

    def _ensure_fragments_for_list_field(self, nested_selection_list, available_fragments, schema):
        """Ensure that fragments are properly available for objects in list fields"""
        if not nested_selection_list or not available_fragments:
            return
            
        # Add all relevant fragments to the nested selection list
        for type_name, fragment_list in available_fragments.items():
            # Only add fragments that are relevant to this selection list's type or its subtypes
            try:
                # Check if this type is compatible with the selection list's type
                target_type = getattr(schema, type_name)
                is_compatible = self._is_type_compatible(nested_selection_list.__type__, target_type, schema)
                
                if is_compatible:
                    if type_name not in nested_selection_list.__fragments__:
                        nested_selection_list.__fragments__[type_name] = []
                    
                    for fragment_data in fragment_list:
                        fragment = self._deserialize_fragment(fragment_data, schema)
                        nested_selection_list.__fragments__[type_name].append(fragment)
            except AttributeError:
                # Type doesn't exist in schema, skip it
                continue

    def _is_type_compatible(self, base_type, target_type, schema):
        """
        Check if target_type is compatible with base_type using schema-based type hierarchy.
        This uses proper GraphQL schema introspection instead of hardcoded type lists.
        """
        # Get type names
        base_name = getattr(base_type, '__name__', str(base_type))
        target_name = getattr(target_type, '__name__', str(target_type))
        
        # Exact match is always compatible
        if base_name == target_name:
            return True
        
        try:
            # Get the actual classes from schema
            base_class = getattr(schema, base_name)
            target_class = getattr(schema, target_name)
            
            # Use Python's issubclass to check if target implements base's interfaces
            # This properly handles the GraphQL interface inheritance:
            # - MaxMetricAttribute implements MaxDomainAttribute interface
            # - MaxNormalAttribute implements MaxDomainAttribute interface  
            # - etc.
            return issubclass(target_class, base_class)
            
        except AttributeError:
            # If either type doesn't exist in schema, they're not compatible
            return False

    def _add_missing_typename_fields(self, json_data):
        """Add missing __typename fields to JSON data for proper polymorphic reconstruction"""
        if isinstance(json_data, dict):
            # Add __typename based on type field if missing
            if 'type' in json_data and '__typename' not in json_data:
                type_mapping = {
                    'metricAttribute': 'MaxMetricAttribute',
                    'normalAttribute': 'MaxNormalAttribute', 
                    'calculatedAttribute': 'MaxCalculatedAttribute',
                    'primaryAttribute': 'MaxPrimaryAttribute',
                    'referenceAttribute': 'MaxReferenceAttribute',
                    'factEntity': 'MaxFactEntity',
                    'dimensionEntity': 'MaxDimensionEntity',
                    'calculated_metric': 'MaxCalculatedMetric'
                }
                
                if json_data['type'] in type_mapping:
                    json_data['__typename'] = type_mapping[json_data['type']]
            
            # Recursively process nested objects
            for key, value in json_data.items():
                if isinstance(value, (dict, list)):
                    json_data[key] = self._add_missing_typename_fields(value)
        
        elif isinstance(json_data, list):
            # Process list items
            return [self._add_missing_typename_fields(item) for item in json_data]
        
        return json_data

    def load_object(self, cache_key: str):
        """Load an sgqlc object from cache"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if not cache_file.exists():
            raise FileNotFoundError(f"Cache file not found: {cache_file}")
        
        with open(cache_file, "r") as f:
            cached_data = json.load(f)
        
        # Import the AnswerRocket schema
        from answer_rocket.graphql.schema import schema
        
        reconstructed_obj = self._recreate_sgqlc_object(cached_data, schema)
        return reconstructed_obj

    def cache_exists(self, cache_key: str) -> bool:
        """Check if a cache file exists for the given key"""
        cache_file = self.cache_dir / f"{cache_key}.json"
        return cache_file.exists()

    def clear_cache(self, cache_key: str = None):
        """Clear cache - specific key or all if no key provided"""
        if cache_key:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if cache_file.exists():
                cache_file.unlink()
        else:
            import shutil
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(exist_ok=True)

    # CacheManagerInterface implementation
    def can_handle(self, data: Any) -> bool:
        """Check if data is an sgqlc BaseType object.
        
        Args:
            data: The data object to check
            
        Returns:
            bool: True if data is an sgqlc BaseType
        """
        return isinstance(data, sgqlc_types.BaseType)
    
    def save(self, cache_file: Path, data: Any, qualname: str) -> Path:
        """Save sgqlc object to JSON file using enhanced serialization.
        
        Args:
            cache_file: Base path for cache file (without extension)
            data: The sgqlc object to save
            qualname: Qualified name of the cached function for logging
        """

        if not isinstance(data, sgqlc_types.BaseType):
            raise ValueError(f"Can only cache sgqlc BaseType objects, got {type(data)}")
        
        # Use enhanced JSON data with polymorphic type fix
        enhanced_json_data = self._add_missing_typename_fields(data.__json_data__.copy())
        
        cache_data = {
            'json_data': enhanced_json_data,
            'class_name': data.__class__.__name__,
            'selection_list': self._serialize_selection_list(data.__selection_list__),
            'schema_name': data.__schema__.__name__ if hasattr(data.__schema__, '__name__') else 'schema'
        }
        
        json_file = cache_file.with_suffix('.json')
        with open(json_file, "w") as f:
            json.dump(cache_data, f)
        
        return json_file

    def load(self, cache_file: Path, qualname: str) -> Any:
        """Load sgqlc object from JSON file.
        
        Args:
            cache_file: Base path for cache file (without extension)
            qualname: Qualified name of the cached function for logging
            
        Returns:
            sgqlc BaseType: The recreated sgqlc object
        """
        json_file = cache_file.with_suffix('.json')
        with open(json_file, "r") as f:
            cached_data = json.load(f)
        
        # Import the AnswerRocket schema
        from answer_rocket.graphql.schema import schema
        return self._recreate_sgqlc_object(cached_data, schema)
    
    def get_file_extension(self) -> str:
        """Return the file extension for sgqlc JSON files.
        
        Returns:
            str: '.json'
        """
        return '.json'