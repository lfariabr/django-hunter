from drf_yasg.generators import OpenAPISchemaGenerator

class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_paths(self, endpoints, components, request=None, public=False):
        paths = super().get_paths(endpoints, components, request, public)
        
        # paths will now be a tuple (path dictionary, prefix)
        if isinstance(paths, tuple):
            path_dict, prefix = paths
        else:
            path_dict = paths
        
        # Filter allowed paths
        allowed_paths = {
            path: path_info for path, path_info in path_dict.items()
            if "auth" in path or path.endswith("recommend/")
        }
        return allowed_paths, prefix  # return the filtered paths and the prefix