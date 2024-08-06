from CTkMessagebox import CTkMessagebox
import pygments

Version = "1.0.0"

LANGUAGES = {
    'txt': 'python',
    'py': 'python',
    'lua': 'lua',
    'luau': pygments.lexers.scripting.LuauLexer,
    'java': 'java',
    'js': 'javascript',
    'c': 'c',
    'h': 'c',
    'cs': pygments.lexers.dotnet.CSharpLexer,
    'cpp': 'c++',
    'hpp': 'c++',
    'css': 'css',
    'html': 'html',
    'json': 'json',
    'rs': 'rust',
    'rb': 'ruby',
    'ts': 'typescript',
    'xml': 'xml',
}

File_Types = [("All Files", "*.*"), ("Text Files", "*.txt"), ("Python Files", "*.py"), ("C Files", ["*.c", "*.h"]),
("Lua Files", ["*.lua", "*.luau"]), ("XML Files", "*.xml"), ("C++ Files", ["*.cpp", "*.hpp"]), ("HTML Files", "*.html"), ("C# Files", "*.css"),
("JSON Files", "*.json"), ("Ruby Files", "*.rb"), ("Rust Files", "*.rs"), ("Java Files", "*.java"), ("JavaScript Files", "*.js")]


def show_messagebox(title, message, icon, options=["OK"]):
    msgbox = CTkMessagebox(title=title, message=message, icon=icon, options=options)
    return msgbox.get()
