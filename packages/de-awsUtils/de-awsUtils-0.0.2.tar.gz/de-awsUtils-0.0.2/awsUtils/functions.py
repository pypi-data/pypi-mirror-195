def splitS3Path(
    s3Path: str):
    s3Path_list = s3Path.replace('s3://', '').split('/')
    Bucket = s3Path_list[0]
    Key = '/'.join(s3Path_list[1:])
    
    return Bucket, Key 