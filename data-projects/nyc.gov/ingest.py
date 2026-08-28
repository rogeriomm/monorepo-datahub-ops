from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (
    ByteType,
    DateType,
    DecimalType,
    IntegerType,
    LongType,
    ShortType,
    StringType,
    StructField,
    StructType,
)

# (field name, field size, Spark data type)
fields = [
    ("PARID", 30, StringType()),
    ("BORO", 1, ByteType()),
    ("BLOCK", 5, StringType()),
    ("LOT", 4, StringType()),
    ("EASE", 1, StringType()),
    ("SUBIDENT_REUC", 10, StringType()),
    ("RECTYPE", 1, ByteType()),
    ("TAXYR", 4, ShortType()),
    ("IDENT", 10, StringType()),
    ("SUBIDENT", 10, StringType()),
    ("ROLL_SECTION", 1, ByteType()),
    ("SECVOL", 5, StringType()),

    ("PYMKTLAND", 12, LongType()),
    ("PYMKTTOT", 12, LongType()),
    ("PYACTLAND", 12, LongType()),
    ("PYACTTOT", 12, LongType()),
    ("PYACTEXTOT", 12, LongType()),
    ("PYTRNLAND", 12, LongType()),
    ("PYTRNTOT", 12, LongType()),
    ("PYTRNEXTOT", 12, LongType()),
    ("PYTXBTOT", 12, LongType()),
    ("PYTXBEXTOT", 12, LongType()),
    ("PYTAXCLASS", 2, StringType()),

    ("TENMKTLAND", 12, LongType()),
    ("TENMKTTOT", 12, LongType()),
    ("TENACTLAND", 12, LongType()),
    ("TENACTTOT", 12, LongType()),
    ("TENACTEXTOT", 12, LongType()),
    ("TENTRNLAND", 12, LongType()),
    ("TENTRNTOT", 12, LongType()),
    ("TENTRNEXTOT", 12, LongType()),
    ("TENTXBTOT", 12, LongType()),
    ("TENTXBEXTOT", 12, LongType()),
    ("TENTAXCLASS", 2, StringType()),

    ("CBNMKTLAND", 12, LongType()),
    ("CBNMKTTOT", 12, LongType()),
    ("CBNACTLAND", 12, LongType()),
    ("CBNACTTOT", 12, LongType()),
    ("CBNACTEXTOT", 12, LongType()),
    ("CBNTRNLAND", 12, LongType()),
    ("CBNTRNTOT", 12, LongType()),
    ("CBNTRNEXTOT", 12, LongType()),
    ("CBNTXBTOT", 12, LongType()),
    ("CBNTXBEXTOT", 12, LongType()),
    ("CBNTAXCLASS", 2, StringType()),

    ("FINMKTLAND", 12, LongType()),
    ("FINMKTTOT", 12, LongType()),
    ("FINACTLAND", 12, LongType()),
    ("FINACTTOT", 12, LongType()),
    ("FINACTEXTOT", 12, LongType()),
    ("FINTRNLAND", 12, LongType()),
    ("FINTRNTOT", 12, LongType()),
    ("FINTRNEXTOT", 12, LongType()),
    ("FINTXBTOT", 12, LongType()),
    ("FINTXBEXTOT", 12, LongType()),
    ("FINTAXCLASS", 2, StringType()),

    ("CURMKTLAND", 12, LongType()),
    ("CURMKTTOT", 12, LongType()),
    ("CURACTLAND", 12, LongType()),
    ("CURACTTOT", 12, LongType()),
    ("CURACTEXTOT", 12, LongType()),
    ("CURTRNLAND", 12, LongType()),
    ("CURTRNTOT", 12, LongType()),
    ("CURTRNEXTOT", 12, LongType()),
    ("CURTXBTOT", 12, LongType()),
    ("CURTXBEXTOT", 12, LongType()),
    ("CURTAXCLASS", 2, StringType()),

    ("PERIOD", 1, ByteType()),
    ("NEWDROP", 1, ByteType()),
    ("NOAV", 1, StringType()),
    ("VALREF", 1, StringType()),
    ("BLDG_CLASS", 2, StringType()),

    ("OWNER", 80, StringType()),
    ("ZONING", 10, StringType()),
    ("HOUSENUM_LO", 12, StringType()),
    ("HOUSENUM_HI", 12, StringType()),
    ("STREET_NAME", 30, StringType()),
    ("ZIP_CODE", 10, StringType()),
    ("GEOSUPPORT_RC", 2, StringType()),
    ("STCODE", 12, StringType()),

    ("LOT_FRT", 8, DecimalType(7, 2)),
    ("LOT_DEP", 8, DecimalType(7, 2)),
    ("LOT_IRREG", 1, StringType()),
    ("BLD_FRT", 8, DecimalType(7, 2)),
    ("BLD_DEP", 8, DecimalType(7, 2)),
    ("BLD_EXT", 2, StringType()),
    ("BLD_STORY", 7, DecimalType(6, 2)),
    ("CORNER", 2, StringType()),

    ("LAND_AREA", 10, LongType()),
    ("NUM_BLDGS", 6, IntegerType()),

    ("YRBUILT", 4, ShortType()),
    ("YRBUILT_RANGE", 4, ShortType()),
    ("YRBUILT_FLAG", 1, StringType()),
    ("YRALT1", 4, ShortType()),
    ("YRALT1_RANGE", 4, ShortType()),
    ("YRALT2", 4, ShortType()),
    ("YRALT2_RANGE", 4, ShortType()),

    ("COOP_APTS", 6, IntegerType()),
    ("UNITS", 6, IntegerType()),

    ("REUC_REF", 20, StringType()),
    ("APTNO", 10, StringType()),
    ("COOP_NUM", 7, StringType()),

    ("CPB_BORO", 1, ByteType()),
    ("CPB_DIST", 2, ByteType()),
    ("APPT_DATE", 8, StringType()),
    ("APPT_BORO", 1, ByteType()),
    ("APPT_BLOCK", 5, StringType()),
    ("APPT_LOT", 4, StringType()),
    ("APPT_EASE", 1, StringType()),

    ("CONDO_NUMBER", 6, StringType()),
    ("CONDO_SFX1", 1, StringType()),
    ("CONDO_SFX2", 1, StringType()),
    ("CONDO_SFX3", 1, StringType()),

    ("UAF_LAND", 12, DecimalType(10, 7)),
    ("UAF_BLDG", 12, DecimalType(10, 7)),

    ("PROTEST_1", 3, StringType()),
    ("PROTEST_2", 3, StringType()),
    ("PROTEST_OLD", 3, StringType()),

    ("ATTORNEY_GROUP1", 4, StringType()),
    ("ATTORNEY_GROUP2", 4, StringType()),
    ("ATTORNEY_GROUP_OLD", 4, StringType()),

    ("GROSS_SQFT", 10, LongType()),
    ("HOTEL_AREA_GROSS", 9, LongType()),
    ("OFFICE_AREA_GROSS", 9, LongType()),
    ("RESIDENTIAL_AREA_GROSS", 9, LongType()),
    ("RETAIL_AREA_GROSS", 9, LongType()),
    ("LOFT_AREA_GROSS", 9, LongType()),
    ("FACTORY_AREA_GROSS", 9, LongType()),
    ("WAREHOUSE_AREA_GROSS", 9, LongType()),
    ("STORAGE_AREA_GROSS", 9, LongType()),
    ("GARAGE_AREA", 9, LongType()),
    ("OTHER_AREA_GROSS", 9, LongType()),

    ("REUC_DESCRIPTION", 500, StringType()),

    ("EXTRACTDT", 8, DateType()),

    # Read T/F fields as strings first.
    ("PYTAXFLAG", 1, StringType()),
    ("TENTAXFLAG", 1, StringType()),
    ("CBNTAXFLAG", 1, StringType()),
    ("FINTAXFLAG", 1, StringType()),
    ("CURTAXFLAG", 1, StringType()),
]


def ingest(spark):
    schema = StructType(
        [
            StructField(name, data_type, True)
            for name, size, data_type in fields
        ]
        + [
            StructField("_TRAILING", StringType(), True)
        ]
    )


    path = "/var/home/rogermm/git/monorepo-datahub-ops-private/data/nyc.gov/PROPMAST_ORE_2027_FIN.txt"


    df = (
        spark.read
        .option("sep", "\t")
        .option("header", False)
        .option("mode", "FAILFAST")
        .option("ignoreLeadingWhiteSpace", True)
        .option("ignoreTrailingWhiteSpace", True)
        .option("dateFormat", "yyyyMMdd")
        .schema(schema)
        .csv(path)
        .drop("_TRAILING")
    )


    # Convert T/F columns to Boolean.
    boolean_columns = [
        "PYTAXFLAG",
        "TENTAXFLAG",
        "CBNTAXFLAG",
        "FINTAXFLAG",
        "CURTAXFLAG",
    ]

    for column in boolean_columns:
        df = df.withColumn(
            column,
            F.when(F.col(column) == "T", F.lit(True))
            .when(F.col(column) == "A", F.lit(False))
            .when(F.col(column).isNull(), F.lit(None).cast("boolean"))
            .otherwise(
                F.raise_error(
                    F.concat(
                        F.lit(f"Invalid boolean value in {column}: "),
                        F.col(column),
                    )
                )
            ),
        )


    # Convert T/F columns to Boolean.
    boolean_columns = [
        "NOAV",
    ]

    for column in boolean_columns:
        df = df.withColumn(
            column,
            F.when(F.col(column) == "Y", F.lit(True))
            .when(F.col(column) == "0", F.lit(False))
            .when(F.col(column).isNull(), F.lit(None).cast("boolean"))
            .otherwise(
                F.raise_error(
                    F.concat(
                        F.lit(f"Invalid boolean value in {column}: "),
                        F.col(column),
                    )
                )
            ),
        )

    return df
