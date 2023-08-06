import boto3
import pandas as pd
from io import BytesIO
import os
from awsUtils.functions import splitS3Path

class S3:
    
    def __init__(self, **kwargs):
        self.s3 = boto3.resource('s3', **kwargs)
        
    def listdir(
        self,
        path: str) -> list:
        """Similar to os.listdir() pyhton method but working with S3

        Parameterssss
        ----------
        path : str

        Returns
        -------
        list
            List of objects in path
        """
        Bucket, Key = splitS3Path(path)
        
        objects = [object.key.split('/')[-1] for object in self.s3.Bucket(Bucket).objects.filter(Prefix=Key)]
                
        return objects
    
    def upload(
        self, 
        localPath: str,
        s3Path: str,
        recursive: bool = False): 
        
        filename = localPath.split('/')[-1]
        Bucket, Key = splitS3Path(s3Path)
        
        if recursive:
            localPath = localPath if localPath.endswith('/') else localPath+'/'
            
            for root, directories, files in os.walk(localPath):
                for file in files:
                    self.s3.Object(Bucket, os.path.join(Key, root.replace(localPath, ''), file))\
                        .upload_file(os.path.join(root, file))
        else:
            self.s3.Object(Bucket, os.path.join(Key, filename)).upload_file(localPath)
        
    
    def read_data(
        self,
        path:str) -> pd.DataFrame:
        """Read Pandas DataFrame directly on S3

        Parameters
        ----------
        path : str

        Returns
        -------
        pd.DataFrame
        """
        Bucket, Key = splitS3Path(path)
        
        if path.endswith('.parquet'):
            data = pd.read_parquet(
                BytesIO(self.s3.Object(Bucket, Key).get()['Body'].read()))
            
        elif path.endswith('.csv'):
            data = pd.read_csv(
                BytesIO(self.s3.Object(Bucket, Key).get()['Body'].read()))
            
        else:
            raise Exception('Data must be csv or parquet format')
            
        return data
    
class Athena:
    
    def __init__(self, **kwargs):
        self.s3 = boto3.client('s3', **kwargs)
        self.athena = boto3.client('athena', **kwargs)
        
    def query(
        self, 
        DataBase: str,
        Catalog: str,
        QueryString: str = None,
        QueryPath: str = None) -> pd.DataFrame:
        """Query AWS Athena and return Pandas DataFrame

        Parameters
        ----------
        QueryString : str
            Query
        QueryPath : str
            Path to .sql file
        DataBase : str
            Athena Database
        Catalog : str
            Athena Catalog

        Returns
        -------
        pd.DataFrame
            Return table as Pandas Data Frame
        """
        assert any([QueryString, QueryPath]), "query expected QueryPath or QueryString"
        assert not all([QueryString, QueryPath]), "query expected one of QueryString or QueryPath not both"
        
        if QueryPath:
            with open(QueryPath, 'r') as inQuery:
                QueryString=inQuery.read().replace('\n', ' ')
             
        execution = self.athena.start_query_execution(
            QueryString=QueryString,
            QueryExecutionContext={
                'Catalog': Catalog,
                'Database': DataBase})
        
        status = self.athena.get_query_execution(QueryExecutionId=execution['QueryExecutionId'])['QueryExecution']['Status']['State']
        print('Running Query. Query ID:', execution['QueryExecutionId'])
        while status in ['QUEUED', 'RUNNING']:
            execution_status = self.athena.get_query_execution(QueryExecutionId=execution['QueryExecutionId'])
            status = execution_status['QueryExecution']['Status']['State']
            
            if status == 'SUCCEEDED':
                print('Query Succeeded! Query ID:', execution['QueryExecutionId'])
                    
            elif status == 'CANCELLED':
                raise Exception('Query Cancelled! Query ID:', execution['QueryExecutionId'])
                
            elif status == 'FAILED':
                
                msg = 'Query Failed! Query ID: ' + execution['QueryExecutionId']+'\n'+\
                      ' Error Message: '+execution_status['QueryExecution']['Status']['AthenaError']['ErrorMessage']
                
                raise Exception(msg)

        Bucket, Key = splitS3Path(execution_status['QueryExecution']['ResultConfiguration']['OutputLocation'])
        
        data = pd.read_csv(
            self.s3.get_object(Bucket=Bucket, Key=Key)['Body'])
        
        self.s3.delete_object(Bucket=Bucket, Key=Key)
        self.s3.delete_object(Bucket=Bucket, Key=Key+'.metadata')
        
        return data