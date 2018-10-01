
# importing some modules.
import boto3
import StringIO
import zipfile
import mimetypes
from botocore.client import Config


#creating name for s3 resource
s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

#creating names for both of the buckets.
portfolio_bucket = s3.Bucket('portfolio.surriya')
build_bucket = s3.Bucket('portfolio-build.surriya')

# Creating portfolio for memory
portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

# Using the zip file to extract it, upload and set the ACL.
with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
            ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
