import os
from functools import wraps
from pydantic import TypeAdapter

from answer_rocket import AnswerRocketClient
from answer_rocket.config import Config
from answer_rocket.chat import Chat
from answer_rocket.data import Data
from answer_rocket.output import OutputBuilder
from answer_rocket.skill import Skill
from answer_rocket.llm import Llm
from answer_rocket.util.cache_manager import TestHarnessCacheManager


class TestHarness:
    '''
    Test harness that uses type-specific cache managers for different data types.
    If run_with_cache is False, the test will run and hit the SDK functions, saving the cache for future runs.
    If run_with_cache is True, the test will run with cache and error if there isn't a cache for a function.
    If lazy_loading is True, cache misses will fallback to real calls and cache the results.
    '''

    run_with_cache = True
    delete_cache = False
    lazy_loading = TypeAdapter(bool).validate_python(os.getenv('LAZY_LOADING', 'true'))
    cache_manager: TestHarnessCacheManager = TestHarnessCacheManager()
     
    def wrapper(self, method):
        @wraps(method)
        def wrapped(cls, *args, **kwargs):
            qualname = method.__qualname__
            print('{!r} executing'.format(qualname))
            cache_key = self.cache_manager.get_cache_key(method, args, kwargs)
            if self.run_with_cache:
                if self.lazy_loading:
                    # Lazy loading: try cache first, fallback to real call if not found
                    try:
                        output = self.cache_manager.load_cache_data(qualname, cache_key)
                        return output
                    except Exception:
                        # Cache miss - execute real call and cache the result
                        output = method(cls, *args, **kwargs)
                        self.cache_manager.save_cache_data(qualname, cache_key, output)
                        return output
                else:
                    # Strict cache mode - fail if cache not found
                    output = self.cache_manager.load_cache_data(qualname, cache_key)
                    return output
            else:
                # Force fresh call mode - always execute real call and cache result
                output = method(cls, *args, **kwargs)
                self.cache_manager.save_cache_data(qualname, cache_key, output)
                return output
        return wrapped
    
    def empty_string_wrapper(self, method):
        @wraps(method)
        def empty_string(cls, *args, **kwargs):
            _ = cls, args, kwargs
            return ""
        return empty_string
    

    def _apply_wrapper_to_class(self, cls, wrapper=None):
        """Apply the wrapper to all methods in an existing class"""
        if wrapper is None:
            wrapper = self.wrapper

        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if callable(attr) and not (attr_name.startswith('__') or attr_name.startswith('_')):
                # Replace the method with a wrapped version
                setattr(cls, attr_name, wrapper(attr))
        return cls
    
    def _test_create_monkey_patch_test(self):

        self._delete_cache()

        # Apply wrapper to all the classes that AnswerRocketClient instantiates
        self._apply_wrapper_to_class(AnswerRocketClient)
        self._apply_wrapper_to_class(Config)
        self._apply_wrapper_to_class(Chat)
        self._apply_wrapper_to_class(Data)
        self._apply_wrapper_to_class(OutputBuilder)
        self._apply_wrapper_to_class(Skill)
        self._apply_wrapper_to_class(Llm, self.empty_string_wrapper)
       

    def _delete_cache(self):
        if self.delete_cache and not self.run_with_cache:
            self.cache_manager.delete_cache()
    
    @staticmethod
    def with_cache(use_cache: bool, lazy_loading: bool = None):
        """
        Decorator to override cache behavior for individual test methods.
        
        Args:
            use_cache: If True, use cache (with lazy_loading behavior if enabled).
                      If False, force fresh calls and save to cache.
            lazy_loading: If True, cache misses will fallback to real calls and cache the results.
                          If None, use the default lazy_loading setting.
        Usage:
            @TestHarness.with_cache(False)  # Force fresh calls for this test
            def test_something(self):
                pass
                
            @TestHarness.with_cache(True)   # Use cache for this test
            def test_something_else(self):
                pass
        """
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # Store original cache setting
                original_run_with_cache = self.__class__.run_with_cache
                original_lazy_loading = self.__class__.lazy_loading
                # Override cache setting for this test
                self.__class__.run_with_cache = use_cache
                if lazy_loading is not None:
                    self.__class__.lazy_loading = lazy_loading

                try:
                    # Run the test with overridden cache setting
                    return func(self, *args, **kwargs)
                finally:
                    # Restore original cache setting
                    self.__class__.run_with_cache = original_run_with_cache
                    self.__class__.lazy_loading = original_lazy_loading
            return wrapper
        return decorator

    @staticmethod
    def with_dataset(dataset_id: str):
        """
        Decorator to override DATASET_ID environment variable for individual test methods.
        
        Args:
            dataset_id: The dataset ID to use for this test
        
        Usage:
            @TestHarness.with_dataset("3c2f7d17-5889-404b-a212-89b8a8bdab7b")
            def test_with_specific_dataset(self):
                pass
        """
        def decorator(func):
            @wraps(func)
            def wrapper(self, *args, **kwargs):
                # Store original dataset ID
                original_dataset_id = os.getenv('DATASET_ID')
                
                # Override dataset ID for this test
                os.environ['DATASET_ID'] = dataset_id
                
                try:
                    # Run the test with overridden dataset ID
                    return func(self, *args, **kwargs)
                finally:
                    # Restore original dataset ID
                    if original_dataset_id is not None:
                        os.environ['DATASET_ID'] = original_dataset_id
                    else:
                        # Remove the key if it wasn't set originally
                        os.environ.pop('DATASET_ID', None)
            
            return wrapper
        return decorator
