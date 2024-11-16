import ast

def extract_routes_with_inputs(file_path):
    routes = []

    # Read and parse the app.py file
    with open(file_path, "r") as file:
        tree = ast.parse(file.read(), filename=file_path)
    
    # Iterate over nodes in the AST
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if (isinstance(decorator, ast.Call) and 
                    isinstance(decorator.func, ast.Attribute) and 
                    decorator.func.attr == "route"):
                    
                    # Extract route path and HTTP methods
                    path = decorator.args[0].s if decorator.args else None
                    methods = next(
                        (kw.value.elts for kw in decorator.keywords if kw.arg == "methods"), None
                    )
                    methods = [method.s for method in methods] if methods else ["GET"]

                    # Extract function parameters and path params
                    func_params = [arg.arg for arg in node.args.args]
                    path_params = [param for param in func_params if param in (path or "")]

                    # Identify JSON body fields in both `data[...]` and `data.get(...)`
                    body_fields = set()
                    for stmt in ast.walk(node):
                        if isinstance(stmt, ast.Subscript):
                            if isinstance(stmt.value, ast.Name) and stmt.value.id == "data":
                                if isinstance(stmt.slice, ast.Constant):
                                    body_fields.add(stmt.slice.value)
                        elif isinstance(stmt, ast.Call):
                            if isinstance(stmt.func, ast.Attribute) and stmt.func.attr == "get":
                                if isinstance(stmt.func.value, ast.Name) and stmt.func.value.id == "data":
                                    if stmt.args and isinstance(stmt.args[0], ast.Constant):
                                        body_fields.add(stmt.args[0].value)

                    routes.append({
                        "function_name": node.name,
                        "route": path,
                        "methods": methods,
                        "path_params": path_params,
                        "json_body_fields": list(body_fields)
                    })

    return routes

# Example usage:
if __name__ == "__main__":
    routes = extract_routes_with_inputs("\aapp.py")
    print(routes)
