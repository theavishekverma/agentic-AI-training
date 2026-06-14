import os
import stat

print("=" * 60)
print("PYTHON os MODULE - COMPREHENSIVE EXAMPLES")
print("=" * 60)

# ─────────────────────────────────────────────
# 1. CURRENT WORKING DIRECTORY
# ─────────────────────────────────────────────
print("\n--- 1. Current Working Directory ---")
cwd = os.getcwd()
print(f"os.getcwd()       : {cwd}")

# ─────────────────────────────────────────────
# 2. DIRECTORY OPERATIONS
# ─────────────────────────────────────────────
print("\n--- 2. Directory Operations ---")

# Create a single directory
os.makedirs("demo_dir/sub_dir", exist_ok=True)
print("os.makedirs()     : Created demo_dir/sub_dir")

# Change working directory
os.chdir("demo_dir")
print(f"os.chdir()        : Changed to {os.getcwd()}")

# List directory contents
files = os.listdir(".")
print(f"os.listdir()      : {files}")

# Go back to original directory
os.chdir("..")

# Rename a directory
os.makedirs("old_name", exist_ok=True)
os.rename("old_name", "new_name")
print("os.rename()       : Renamed old_name -> new_name")

# Remove empty directory
os.rmdir("new_name")
print("os.rmdir()        : Removed new_name")

# Remove directory tree
os.makedirs("to_delete/a/b", exist_ok=True)
os.removedirs("to_delete/a/b")   # removes all empty dirs in path
print("os.removedirs()   : Removed to_delete/a/b (empty chain)")

# ─────────────────────────────────────────────
# 3. FILE OPERATIONS
# ─────────────────────────────────────────────
print("\n--- 3. File Operations ---")

# Create and write a file using low-level os.open
fd = os.open("demo_dir/sample.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.write(fd, b"Hello from os.write!\n")
os.close(fd)
print("os.open/write/close: Created demo_dir/sample.txt")

# Read with os.open
fd = os.open("demo_dir/sample.txt", os.O_RDONLY)
data = os.read(fd, 100)
os.close(fd)
print(f"os.read()         : {data.decode().strip()}")

# Rename a file
os.rename("demo_dir/sample.txt", "demo_dir/renamed.txt")
print("os.rename()       : sample.txt -> renamed.txt")

# Check if path exists
print(f"os.path.exists()  : {os.path.exists('demo_dir/renamed.txt')}")

# Remove a file
os.remove("demo_dir/renamed.txt")
print("os.remove()       : Deleted renamed.txt")

# ─────────────────────────────────────────────
# 4. PATH OPERATIONS (os.path)
# ─────────────────────────────────────────────
print("\n--- 4. os.path Operations ---")

p = "/home/user/documents/report.pdf"

print(f"os.path.basename()  : {os.path.basename(p)}")       # report.pdf
print(f"os.path.dirname()   : {os.path.dirname(p)}")        # /home/user/documents
print(f"os.path.split()     : {os.path.split(p)}")          # tuple
print(f"os.path.splitext()  : {os.path.splitext(p)}")       # ('...', '.pdf')
print(f"os.path.join()      : {os.path.join('/home','user','file.txt')}")
print(f"os.path.abspath()   : {os.path.abspath('.')}")
print(f"os.path.isfile()    : {os.path.isfile(p)}")
print(f"os.path.isdir()     : {os.path.isdir('demo_dir')}")
print(f"os.path.isabs()     : {os.path.isabs(p)}")
print(f"os.path.getsize()   : {os.path.getsize(os.path.abspath(__file__))} bytes")

# ─────────────────────────────────────────────
# 5. ENVIRONMENT VARIABLES
# ─────────────────────────────────────────────
print("\n--- 5. Environment Variables ---")

# Get an env variable (with default)
home = os.environ.get("HOME") or os.environ.get("USERPROFILE", "Not set")
print(f"os.environ.get()  : HOME = {home}")

# Set an env variable (only for this process)
os.environ["MY_VAR"] = "hello_world"
print(f"os.environ set    : MY_VAR = {os.environ['MY_VAR']}")

# Delete an env variable
del os.environ["MY_VAR"]
print("os.environ del    : MY_VAR removed")

# List all env variable names
print(f"os.environ keys   : {len(os.environ)} environment variables present")

# Using os.getenv (shorthand)
path_val = os.getenv("PATH", "Not found")
print(f"os.getenv()       : PATH starts with '{path_val[:40]}...'")

# ─────────────────────────────────────────────
# 6. PROCESS INFORMATION
# ─────────────────────────────────────────────
print("\n--- 6. Process Information ---")

print(f"os.getpid()       : Current PID  = {os.getpid()}")
print(f"os.getppid()      : Parent PID   = {os.getppid()}")
print(f"os.cpu_count()    : CPU cores    = {os.cpu_count()}")
print(f"os.name           : OS name      = {os.name}")          # 'nt' on Windows, 'posix' on Linux/Mac
print(f"os.sep            : Path sep     = '{os.sep}'")
print(f"os.linesep        : Line sep     = {repr(os.linesep)}")
print(f"os.curdir         : Current dir  = '{os.curdir}'")
print(f"os.pardir         : Parent dir   = '{os.pardir}'")
print(f"os.extsep         : Ext sep      = '{os.extsep}'")

# ─────────────────────────────────────────────
# 7. WALKING A DIRECTORY TREE
# ─────────────────────────────────────────────
print("\n--- 7. os.walk() - Directory Tree ---")

# Create a small tree to walk
os.makedirs("demo_dir/a/b", exist_ok=True)
with open("demo_dir/a/file1.txt", "w") as f: f.write("file1")
with open("demo_dir/a/b/file2.txt", "w") as f: f.write("file2")

for root, dirs, files in os.walk("demo_dir"):
    level = root.replace("demo_dir", "").count(os.sep)
    indent = "  " * level
    print(f"{indent}[dir]  {os.path.basename(root)}/")
    for file in files:
        print(f"{indent}  [file] {file}")

# ─────────────────────────────────────────────
# 8. os.scandir() — faster than listdir for metadata
# ─────────────────────────────────────────────
print("\n--- 8. os.scandir() ---")
with os.scandir("demo_dir") as entries:
    for entry in entries:
        kind = "DIR " if entry.is_dir() else "FILE"
        print(f"  {kind}  {entry.name:20s}  path={entry.path}")

# ─────────────────────────────────────────────
# 9. FILE STATS
# ─────────────────────────────────────────────
print("\n--- 9. os.stat() - File Metadata ---")
script_stat = os.stat(__file__)
print(f"os.stat().st_size   : {script_stat.st_size} bytes")
print(f"os.stat().st_mtime  : {script_stat.st_mtime:.0f} (unix timestamp)")
print(f"os.stat().st_mode   : {oct(script_stat.st_mode)}")

# ─────────────────────────────────────────────
# 10. RUNNING SYSTEM COMMANDS
# ─────────────────────────────────────────────
print("\n--- 10. os.system() ---")
ret = os.system("echo Hello from os.system")
print(f"Return code: {ret}")

# ─────────────────────────────────────────────
# 11. os.path.expanduser / expandvars
# ─────────────────────────────────────────────
print("\n--- 11. Path Expansion ---")
print(f"os.path.expanduser('~')   : {os.path.expanduser('~')}")
print(f"os.path.expandvars('%OS%'): {os.path.expandvars('%OS%')}")

# ─────────────────────────────────────────────
# 12. SYMBOLIC LINKS (Linux/Mac) / os.link (hardlink)
# ─────────────────────────────────────────────
print("\n--- 12. Links ---")
with open("demo_dir/original.txt", "w") as f:
    f.write("original")
try:
    os.symlink("demo_dir/original.txt", "demo_dir/symlink.txt")
    print(f"os.symlink()      : Created symlink.txt")
    print(f"os.path.islink()  : {os.path.islink('demo_dir/symlink.txt')}")
    print(f"os.readlink()     : {os.readlink('demo_dir/symlink.txt')}")
    os.unlink("demo_dir/symlink.txt")
except (OSError, NotImplementedError):
    print("os.symlink        : Requires privileges on Windows (skipped)")

# ─────────────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────────────
print("\n--- Cleanup ---")
import shutil
shutil.rmtree("demo_dir", ignore_errors=True)
print("Removed demo_dir tree.")

print("\n" + "=" * 60)
print("All os module examples completed!")
print("=" * 60)
