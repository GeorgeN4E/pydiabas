class ECU():
    NAME = ""

    def __init__(self, name=None) -> None:
        if name is not None:
            self.NAME = name
        

    def get_jobs(self, connection, details: bool=True, verbose: bool=False) -> list[dict]:

        # Fill a list with available job names from ECU
        jobs = {job["JOBNAME"]: {} for job in connection.job(self.NAME, "_JOBS")[1:]}

        if verbose:
            print(f"Found {len(jobs)} jobs")

        if details:
            # Get additional data for all found jobs
            for n, job in enumerate(jobs):
                
                # Get job comments, argument and return value information
                jobs[job] = self.get_job_details(connection, job)

                if verbose:
                    percent = round(100 * (n + 1) / len(jobs))
                    print(f"\r[{'=' * (percent // 2)}{' ' * (50 - (percent // 2))}] {percent:3d}% complete", end="")

        if verbose:
            print("\nDone!")
        
        return jobs
    

    def get_job_details(self, connection, job: str) -> dict:
        try:
            # All comments will be stored in set 1
            comments = connection.job(self.NAME, "_JOBCOMMENTS", job)[1]
        except IndexError:
            comments = {}

        # Argument and result info will be stored in set 1-n
        try:
            arguments = connection.job(self.NAME, "_ARGUMENTS", job)[1:]
        except IndexError:
            arguments = [{}]

        try:
            results = connection.job(self.NAME, "_RESULTS", job)[1:]
        except IndexError:
            arguments = [{}]
        
        # Get job comments, argument and return value information
        info = {
            "comments": [
                comments[key] for key in sorted(
                    comments.keys(),
                    key=lambda x: int(x.replace("JOBCOMMENT", ""))
                )
            ],
            "arguments": [{
                "name": arguments[i]["ARG"],
                "type": arguments[i]["ARGTYPE"],
                "comments": [arguments[i][key] for key in arguments[i].keys() if key.startswith("ARGCOMMENT")]
            } for i in range(len(arguments))],
            "results": [{
                "name": results[i]["RESULT"],
                "type": results[i]["RESULTTYPE"],
                "comments": [results[i][key] for key in results[i].keys() if key.startswith("RESULTCOMMENT")]
            } for i in range(len(results))],
        }

        return info
        

    def get_tables(self, connection, details: bool=True, verbose: bool=False) -> dict[dict]:

        # Fill a dict with all available table names as keys
        tables = {table["TABLE"]: {} for table in connection.job(self.NAME, "_TABLES")[1:]}

        if verbose:
            print(f"Found {len(tables)} tables")

        if details:
            # Get additional information for all tables
            for n, table in enumerate(tables):                
                tables[table] = self.get_table_details(connection, table)

                if verbose:
                    percent = round(100 *(n + 1) / len(tables))
                    print(f"\r[{'=' * (percent / 2)}{' ' * (50 - (percent / 2))}] {percent:3d}% complete", end="")
        
        if verbose:
            print("\nDone!")
        
        return tables


    def get_table_details(self, connection, table: str) -> dict:
        # Get column headers and table body data
        # Column names will be in set 1, all data rows will be in the following sets
        try:
            contents = connection.job(self.NAME, "_TABLE", table)[1:]
        except IndexError:
            contents = [{}]

        print(contents)
        
        info = {
            "header": [
                contents[0][key] for key in sorted(
                    contents[0].keys(),
                    key=lambda x: int(x.replace("COLUMN", ""))
                )
            ] if contents else [],
            "body":  [
                [
                    contents[1:][i][key] for key in sorted(
                        contents[1:][i].keys(),
                        key=lambda x: int(x.replace("COLUMN", ""))
                    )
                ] for i in range(len(contents[1:]))
            ]
        }

        return info
