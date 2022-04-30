from tabulate import tabulate
import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime


class TestAnalyzer:
    def __init__(self):
        self.bar_graph()
        self.table()

    def bar_graph(self):
        with open('./json_data/test_assert_statements.json', 'r') as f:
            content = json.load(f)
        f.close()
        graph_data = {}
        for k, v in content.items():
            if len(v) == 0:
                continue
            graph_data[k[12:]] = len(v)

        graph_data = dict(sorted(graph_data.items(), key = lambda x: x[1], reverse = True))

        plt.figure(figsize=(50, 10))
        plt.rcParams['figure.dpi'] = 800
        plt.bar(list(graph_data.keys()), list(graph_data.values()))
        plt.title('Files with Assert statements')
        plt.xlabel('File Name')
        plt.ylabel('Number of Assert statements')
        plt.savefig('./figures/test_assert_statements.png')

    def table(self):
        with open('./json_data/test_assert_statements.json', 'r') as f:
            content = json.load(f)
        f.close()

        headers = [["Test File Name", "Number of Assert Statements", "Location of Assert Statements (Line Numbers)"]]
        table = []

        for file, statements in content.items():
            if len(statements) > 0:
                table.append([file, len(statements), statements])

        table.sort(key=lambda x: x[1], reverse=True)

        table = headers + table

        with open('./figures/test_analysis.txt', "w") as f:
            f.write(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
            f.close()


class ProductionAnalyzer():
    def __init__(self):
        self.table()

    def table(self):
        with open('./json_data/production_assert_statements.json', 'r') as f:
            assert_statements = json.load(f)
            f.close()

        with open('./json_data/production_debug_statements.json', 'r') as f:
            debug_statements = json.load(f)
            f.close()

        files = list(set(debug_statements.keys()).union(set(assert_statements.keys())))

        headers = [["File Name", "Number of Assert Statements", "Number of Debug Statements", "Location of Assert Statements (Line Numbers)", "Location of Debug Statements (Line Numbers)"]]
        table = []

        for file in files:
            table.append([file, len(assert_statements[file]), len(debug_statements[file]), assert_statements[file], debug_statements[file]])

        for row in table:
            if row[1] == 0 and row[2] == 0:
                table.remove(row)

        table = headers + table

        with open('./figures/production_analysis.txt', "w") as f:
            f.write(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
            f.close()

class CommitAnalyzer():
    def __init__(self):
        # self.project()
        self.files_added()
        # self.commits()
        # self.file_commits()

    def project(self):
        commit_dates = []
        with open('./json_data/commit_dates.json', 'r') as f:
            content = json.load(f)
            f.close()

        for file, dates in content.items():
            for date in dates:
                commit_dates.append(datetime.strptime(date, '%d-%m-%y'))

        commit_dates.sort()

        date_count = Counter(commit_dates)

        plt.figure(figsize=(20, 10))
        plt.rcParams['figure.dpi'] = 300
        plt.plot(list(date_count.keys()), list(date_count.values()))
        plt.title("Project Test Commit History")
        plt.xlabel("Year")
        plt.ylabel("Number of Commits")
        plt.savefig("./figures/project_commit_history.png", bbox_inches='tight')

    def files_added(self):
        added_dates = {}
        with open('./json_data/commit_dates.json', 'r') as f:
            content = json.load(f)
            f.close()

        for file, dates in content.items():
            added_dates[file] = datetime.strptime(min(dates), '%d-%m-%y')

        date_count = Counter(list(added_dates.values()))

        plt.figure(figsize=(40, 10))
        plt.rcParams['figure.dpi'] = 300
        plt.bar(list(date_count.keys()), list(date_count.values()), width=12)
        plt.title("History of adding test files")
        plt.xlabel("Year")
        plt.ylabel("Number of Files Added")
        plt.savefig("./figures/file_added_history.png", bbox_inches='tight')


    def commits(self):
        top_authors = []
        with open('./json_data/commit_authors.json', 'r') as f:
            content = json.load(f)
            f.close()

        for file, authors in content.items():
            top_authors.extend(authors)

        top_authors.sort(reverse=True)

        commit_count = Counter(top_authors)

        sorted_commits = dict(sorted(commit_count.items(), key = lambda x: x[1], reverse = True))

        plt.figure(figsize=(40, 10))
        plt.rcParams['figure.dpi'] = 500
        plt.bar(list(sorted_commits.keys())[:7], list(sorted_commits.values())[:7])
        plt.title("Top Testing Contributors")
        plt.xlabel("Author Name")
        plt.ylabel("Number of Files contibuted")
        plt.savefig("./figures/top_authors.png", bbox_inches='tight')

    def file_commits(self):
        with open('./json_data/total_commits.json', 'r') as f:
            content = json.load(f)
            f.close()

        top_commits = {}

        for k, v in content.items():
            top_commits[k[12:]] = v

        top_commits = dict(sorted(top_commits.items(), key=lambda x: x[1], reverse=True))

        plt.figure(figsize=(60, 10))
        plt.rcParams['figure.dpi'] = 600
        plt.bar(list(top_commits.keys())[:20], list(top_commits.values())[:20])
        plt.title("Top Files")
        plt.xlabel("File Name")
        plt.ylabel("Number of Commits")
        plt.savefig("./figures/top_files.png", bbox_inches='tight')

if __name__ == '__main__':
    plt.rcParams.update({'font.size': 30})
    # TestAnalyzer()
    # ProductionAnalyzer()
    CommitAnalyzer()