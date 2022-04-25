import os
import re
from pydriller import Repository
import json


REPO_PATH = './ompi'
PRODUCTION_PATH = './ompi/ompi'
TEST_PATH = './ompi/test'

def handle_repo():
    file_list = os.listdir('./')
    print(file_list)

    if 'ompi' not in file_list:
        print("Repo not found. Cloning now ...")
        os.system('git clone https://github.com/open-mpi/ompi.git')
        print("Cloning done")

def get_files(path):       
        file_list = os.listdir(path)

        all_files = []

        for file in file_list:
            full_path = os.path.join(path, file)
            if file.endswith(".c"):
                all_files.append(full_path)
            elif os.path.isdir(full_path):
                all_files += get_files(full_path)

        return all_files

class TestAnalyzer():  

    def __init__(self):
        print("Starting test analyzer")

        test_files = get_files(TEST_PATH)
        assert_statements = self.count_asserts(test_files)
        self.create_report(test_files, assert_statements)
        self.write_json(assert_statements)

        print("Test analysis complete \n")


    def count_asserts(self, files):
        assert_statements = {}

        for file in files:
            with open(file) as f:
                lines = f.readlines()
                locations = []
                for i, line in enumerate(lines):
                    find = re.findall('assert', line)
                    if find:
                        locations.append(i + 1)

                assert_statements[file] = locations
            f.close()

        return assert_statements


    def create_report(self, test_files, assert_statements):

        total_asserts = 0
    
        for file, asserts in assert_statements.items():
            if len(asserts) > 0:
                total_asserts += 1

        percentatge = (total_asserts * 100) // len(test_files)

        with open('./reports/test_analysis.txt', "w") as f:
            f.write("\nTotal Number of Test Files = " + str(len(test_files)))
            f.write("\nTotal Number of Test Files with Assert Statements = " +  str(total_asserts))       
            f.write("\nPercentage = " +  str(percentatge) + "%")
            f.close()

    def write_json(self, assert_statements):
        with open("./json_data/test_assert_statements.json", "w") as f:
            json.dump(assert_statements, f)
            f.close()


class ProductionAnalyzer():

    def __init__(self):
        print("Starting Production Analyzer")

        production_files = get_files(PRODUCTION_PATH)
        assert_statements, debug_statements = self.count_debug_assert(production_files)
        self.create_report(production_files, assert_statements, debug_statements)
        self.write_json(assert_statements, debug_statements)

        print("Production analysis complete \n")

      
    def count_debug_assert(self, files):
        debug_statements = {}
        assert_statements = {}

        for file in files:
            with open(file) as f:
                lines = f.readlines()
                asserts = []
                debugs = []
                for i, line in enumerate(lines):
                    assert_search = re.search('assert', line)
                    debug_search = re.search('DEBUG', line)
                    if assert_search:
                        asserts.append(i+1)
                    if debug_search:
                        debugs.append(i+1)
                if asserts or debugs:
                    assert_statements[file] = asserts
                    debug_statements[file] = debugs
            f.close()

        return assert_statements, debug_statements


    def create_report(self, files, assert_statements, debug_statements):
        total_asserts, total_debugs = 0, 0

        for file, statements in assert_statements.items():
            if len(statements) > 0:
                total_asserts += 1
        for file, statements in debug_statements.items():
            if len(statements) > 0:
                total_debugs += 1

        percentage_asserts = (total_asserts * 100) // len(files)
        percentage_debugs = (total_debugs * 100) // len(files)

        with open("./reports/production_analysis.txt", "w") as f:
            f.write("\nTotal Number of Production Files = " + str(len(files)))
            f.write("\nTotal Number of Files with Assert Statements = " +  str(total_asserts))       
            f.write("\nTotal Number of Files with Debug Statements = " +  str(total_debugs))    
            f.write("\nPercentage of Files with Assert Statements = " + str(percentage_asserts) + "%")
            f.write("\nPercentage of Files with Debug Statements = " + str(percentage_debugs) + "%")
            f.close()


    def write_json(self, assert_statements, debug_statements):
        with open("./json_data/production_assert_statements.json", "w") as f:
            json.dump(assert_statements, f)
            f.close()

        with open("./json_data/production_debug_statements.json", "w") as f:
            json.dump(debug_statements, f)
            f.close()


class CommitAnalyzer():

    def __init__(self):
        print("Starting commit analyzer")
        print("This will take a while to complete...")

        test_files = get_files(TEST_PATH)
        total_commits, commit_authors, commit_dates = self.get_commit_details(test_files)
        self.create_report(total_commits, commit_authors, commit_dates)
        self.write_json(total_commits, commit_authors, commit_dates)

        print("Commit Analyzer finished \n")
        

    def get_commit_details(self, files):
        total_commits = {}
        commit_authors = {}
        commit_dates = {}
        for file in files:
            print("Analyzing File ", file[7:])
            authors = []
            dates = []
            commit_count = 0
            commits = Repository(REPO_PATH, filepath=file[7:]).traverse_commits()
            
            for commit in commits:
                commit_count += 1
                authors.append(commit.author.name)
                date = commit.author_date
                dates.append("{:%d-%m-%y}".format(date))

            commit_authors[file] = list(set(authors))
            commit_dates[file] = dates
            total_commits[file] = commit_count
        
        return total_commits, commit_authors, commit_dates

    def create_report(self, total_commits, commit_authors, commit_dates):
        
        headers = [["File Name", "Date Added", "Authors", "Total Commits"]]
        table = []
        total_authors = []
        for file, commits in total_commits.items():
            table.append([file, commit_dates[file][0], commit_authors[file], commits])
            total_authors.extend(commit_authors[file])

        table = headers + table

        with open('./reports/commit_analysis.txt', "w") as f:
            f.write("\nTotal Number of Authors = " + str(len(set(total_authors))))
            f.close()

    def write_json(self, total_commits, commit_authors, commit_dates):
        with open("./json_data/total_commits.json", "w") as f:
            json.dump(total_commits, f)
            f.close()

        with open("./json_data/commit_authors.json", "w") as f:
            json.dump(commit_authors, f)
            f.close()

        with open("./json_data/commit_dates.json", "w") as f:
            json.dump(commit_dates, f)
            f.close()


if __name__ == '__main__':
    handle_repo()
    TestAnalyzer()
    ProductionAnalyzer()
    CommitAnalyzer()
    