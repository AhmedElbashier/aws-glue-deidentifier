from pyspark.sql.functions import lit, substring
from awsglue.dynamicframe import DynamicFrame
from awsglue.dynamicframe import DynamicFrameCollection

def MyTransform(glueContext, dfc) -> DynamicFrameCollection:
    df = dfc.select(list(dfc.keys())[0]).toDF()

    # De-identify data
    df = df.withColumn("patient_name", lit("REDACTED"))
    df = df.withColumn("dob", substring("dob", 1, 4))
    df = df.withColumn("phone", lit("XXXXXXX"))
    df = df.withColumn("address", lit("REDACTED"))

    output = DynamicFrame.fromDF(df, glueContext, "output")
    return DynamicFrameCollection({"CustomTransform": output}, glueContext)
