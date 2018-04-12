import os
import sys
import xml.etree.ElementTree as ET
import subprocess
import shutil

def main():
    PRODUCT_FLAVOR = None
    PROJECT_ROOT = None
    
    if len(sys.argv) < 2 or not os.path.exists(sys.argv[1]):
        print("Error: There is missing argument.")
        sys.exit(1)
    PROJECT_ROOT = sys.argv[1]
    if len(sys.argv) >= 3:
        PRODUCT_FLAVOR = sys.argv[2]

    modules = {}

    for line in sys.stdin:
        line = line.strip()
        if line != '' and os.path.exists(line):
            module = line[len(PROJECT_ROOT):]
            while module[0] == os.sep:
                module = module[1:]
            folders = module.split(os.sep)
            if len(folders) == 1 or not os.path.exists(PROJECT_ROOT + "/" + folders[0] + "/build.gradle"):
                continue
            modules[folders[0]] = 1


    lint_results_dir = PROJECT_ROOT + "/build/lint"
    if os.path.exists(lint_results_dir):
        shutil.rmtree(lint_results_dir)
    os.makedirs(lint_results_dir)

    failedModules = {}
    issues = {}
    for module in modules:
        issuesModule = issues[module] = {}
        gradlew = PROJECT_ROOT + "/gradlew"
        report_dir = PROJECT_ROOT + "/" + module + "/build/reports"
        report_filename = "lint-results"
        if PRODUCT_FLAVOR is not None:
            report_filename += "-" + PRODUCT_FLAVOR[0].lower() + PRODUCT_FLAVOR[1:]
        report_xml = report_dir + "/" + report_filename + ".xml"
        report_html = report_dir + "/" + report_filename + ".html"
        cmd = gradlew + " " + module + ":lint" + PRODUCT_FLAVOR
        print(cmd)
        process = subprocess.Popen([gradlew, module + ":lint" + PRODUCT_FLAVOR])
        process.wait()
        if process.returncode != 0:
            print("Error: Lint failed on module " + module)
            failedModules[module] = 1
            continue
        
        print("Parsing: " + report_xml)
        if not os.path.exists(report_xml):
            print("Error: Lint result not found on module " + module)
            failedModules[module] = 1
            continue
        xml = ET.parse(report_xml)
        root = xml.getroot()
        for issue in root:
            severity = issue.attrib['severity']
            if severity not in issuesModule:
                issuesModule[severity] = 1
            else:
                issuesModule[severity] += 1
        shutil.copyfile(report_xml, lint_results_dir + "/" + module + "-" + report_filename + ".xml")
        shutil.copyfile(report_html, lint_results_dir + "/" + module + "-" + report_filename + ".html")

    abort = False
    print("Lint Result:")
    if len(issues) == 0:
        print("No changed module.")
    else:
        errors = 0
        for module in issues:
            issuesModule = issues[module]
            print(module)
            if len(issuesModule) != 0:
                print("Found issue(s):")
                issueStr = ""
                for sev in issuesModule:
                    issueStr += str(issuesModule[sev]) + " " + sev + "(s); "
                    if sev == "Error" or sev == "Fatal":
                        errors += issuesModule[sev]
                print(issueStr)
            else:
                print("No issue found.")
            print("")
        
        if errors !=0:
            print("Error: Lint failed because there are some error or fatal issues found.")
            abort = True

    if len(failedModules) != 0:
        print("Error: Lint failed on several modules:")
        moduleList = ""
        for module in failedModules:
            moduleList += module + "; "
        print(moduleList)
        abort = True
    
    if abort:
        sys.exit(1)

if __name__ == "__main__":
    main()