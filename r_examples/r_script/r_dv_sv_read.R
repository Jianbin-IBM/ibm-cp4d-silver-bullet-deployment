"Hello Wolrd"

library("reticulate")
suppressPackageStartupMessages(library("arrow"))

itcfs <- import("itc_utils.flight_service")

readClient <- itcfs$get_flight_client()

# NOTE:
#  A limit of 5000 rows has been applied to the request to enable sample previewing.
#  Adjust the display message as needed by editing the following lines:
library(IRdisplay)
display_html("A row limit of 5000 has been applied to the query to enable sample previewing. If the data set is larger, only the first 5000 rows will be loaded.")
#  Edit select_statement to change or disable the row limit.
#
Db2oltp_1tb_data_request = dict(
    "connection_name" = "Db2oltp-1tb",
    "interaction_properties" = dict(
        "select_statement" = "SELECT * FROM \"ANZ\".\"BANK_SAVINGS\" FETCH FIRST 5000 ROWS ONLY"
    )
)

flightInfo <- itcfs$get_flight_info(readClient, nb_data_request=Db2oltp_1tb_data_request)

tables <- itcfs$read_tables(readClient, flightInfo, timeout=240)
data_df_1 <- as.data.frame(tables[[1]])
print(head(data_df_1))


library(ibmWatsonStudioLib)
wslib <- access_project_or_space()

Db2oltp_1tb_metadata = wslib$get_connection("Db2oltp-1tb")

library(RJDBC)

drv <- JDBC(driverClass="com.ibm.db2.jcc.DB2Driver", classPath="/opt/jdbc/db2jcc4.jar")

Db2oltp_1tb_url <- paste("jdbc:db2://",
    Db2oltp_1tb_metadata[][["host"]],
    ":", Db2oltp_1tb_metadata[][["port"]],
    "/", Db2oltp_1tb_metadata[][["database"]],
    ":", "sslConnection=true;",
    sep=""
)

Db2oltp_1tb_connection <- dbConnect(drv,
    Db2oltp_1tb_url,
    Db2oltp_1tb_metadata[][["username"]],
    Db2oltp_1tb_metadata[][["password"]]
)

# NOTE:
#  A row limit has been applied to the query to enable sample previewing.
#  Adjust the display message and query as needed by editing the following lines:
library(IRdisplay)
display_html("A row limit of 5000 has been applied to the query to enable sample previewing. If the data set is larger, only the first 5000 rows will be loaded.")
query <- "SELECT * FROM \"ANZ\".\"BANK_SAVINGS\" FETCH FIRST 5000 ROWS ONLY"

data <- dbSendQuery(Db2oltp_1tb_connection, query)
# fetch first 5 rows
data_df_2 <- dbFetch(data, n = 5)
print(head(data_df_2))

# After use, close the database connection with the following code:
# dbDisconnect(Db2oltp_1tb_connection)

library("reticulate")
suppressPackageStartupMessages(library("arrow"))

itcfs <- import("itc_utils.flight_service")

readClient <- itcfs$get_flight_client()

storage_volume_data_request = dict(
    "connection_name" = "storage volume",
    "interaction_properties" = dict(
        #"row_limit" = 5000,
        "file_name" = "ANZ/BANK_SAVINGS.csv",
        "infer_schema" = "true",
        "infer_as_varchar" = "false"
    )
)

flightInfo <- itcfs$get_flight_info(readClient, nb_data_request=storage_volume_data_request)

tables <- itcfs$read_tables(readClient, flightInfo, timeout=240)
data_df_3 <- as.data.frame(tables[[1]])
print(head(data_df_3))

library("reticulate")
suppressPackageStartupMessages(library("arrow"))

itcfs <- import("itc_utils.flight_service")

readClient <- itcfs$get_flight_client()

nb_data_request = dict(
    "data_name" = "data.csv",
    "interaction_properties" = dict(
        #"row_limit" = 500,
        "infer_schema" = "true",
        "infer_as_varchar" = "false"
    )
)

flightInfo <- itcfs$get_flight_info(readClient, nb_data_request=nb_data_request)

tables <- itcfs$read_tables(readClient, flightInfo, timeout=240)
data_df_5 <- as.data.frame(tables[[1]])
print(head(data_df_5))