from xfctRft import robotFileUtils
args = ["keywords::variables/variables-fat.json::resourceset-controller/resourceset-page.json"]
file_path = args[-1]
robotFileUtils.generate_robot_file_by_file_path(file_path)
robotFileUtils.run_case(args)