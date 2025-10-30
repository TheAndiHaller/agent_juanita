from functions.get_files_info import get_files_info

try:
    print(get_files_info("calculator", "."))
    print(get_files_info("calculator", "pkg"))
    print(get_files_info("calculator", "/bin"))
    print(get_files_info("calculator", "../"))
except Exception as e:
    print(f"Error: {e}")