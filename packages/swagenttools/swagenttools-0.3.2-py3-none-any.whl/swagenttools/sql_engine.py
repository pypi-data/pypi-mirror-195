import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


################################################################
#                        SQL_ENGINE                            #
################################################################
class SQLEngine():

    def __init__(self, loadfile='sql_functions/swagent_main_db_create.sql'):
        self.engine = None
        self.filename = loadfile

        # extract the functions found in the file passed.
        self.sql_functions = {}
        with open(loadfile, 'r') as f:
            r = list(filter(None, f.read().split("\n--")))
            for rr in r:
                sql_func_name = rr.split('\n', 1)[0]
                sql_query = rr.split('\n', 1)[1]
                self.sql_functions[sql_func_name] = sql_query

    def run_sql(self, sql_query):
        session = scoped_session(sessionmaker(bind=self.engine))
        try:
            session.execute(sql_query)
            session.commit()
            print('Ran query successfully!')
        except Exception as error:
            print('Error while running query to PostgreSQL', error)
        finally:
            session.close()
            print('Closing Session!')

    def get_predef(self, functioname):
        # return the function asked for
        if functioname in self.sql_functions:
            return self.sql_functions[functioname]

    
    def db_connect(self, db, envpath, host='localhost', port='5432'):
        """ > makes connection with specified database
            ________________________________________________________
            
            params:
                - envpath: path to the environment file assigned 
                the password/username for the db.
                -db: name of db from where to make changes or extract 
                data.
                - port: port adress, default 5432
                - host: host address, default localhost 

            returns:
                - the engine after a connection has been established.
        """

        # locate the environment variables
        load_dotenv(envpath, override=True)
        DATABASE_USER = os.getenv("USER")
        DATABASE_PASSWORD = os.getenv("PASSWORD")

        try:
            # connection string contains all necessary info
            connection_string = "postgresql://{}:{}@{}:{}/{}".format(DATABASE_USER, DATABASE_PASSWORD, host, port, db)
            engine = create_engine(connection_string)
            # log connection established. 
            print("\nYou are connected to --->", engine.url.database, "\n") 
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if engine is not None:
                self.engine = engine # return engine only


    def load_batch_to_DB(self, batch, where, row_key):
        """ > appends the newly found data to the full_replays db.
            _______________________________________________________

            params:
                - batch: dataframe with new data (size X)
                - connection: the engine or conn format variable
        """
        try:
            # start a count
            error_cnt = 0
            for i, row in batch.iterrows():
                # get the results of the next value to append 
                sql = 'SELECT * FROM {} WHERE {} = {};'.format(where, row_key,  row[row_key])
                found = pd.read_sql(sql, con=self.engine)

                # if value found in db dont add else add
                if len(found) == 0:
                    batch.iloc[i:i+1].to_sql(name=where, if_exists='append', con=self.engine, index=False)
                else:
                    error_cnt += 1

            # print the amount of results that were actually added to the db    
            print("{} new {} were added...".format(row_key, len(batch) - error_cnt))
        except Exception as error:
            print('Error while appending to PostgreSQL', error)


if __name__ == '__main__':
    
    engine = SQLEngine(loadfile='sql_functions/swagent_main_db_create.sql')
    engine.db_connect(db="swagent", envpath="/home/oulex/secrets/swagent_db.env")
    
    
