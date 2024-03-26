# DO NOT modify file name since we pre-defined it as "install_r_pkgs.R"

# Action: Please update the List of packages to install here
packages_to_install <- c(
  "jsonlite", "xgboost", "devtools"
)

# DO NOT modify below code
options(repos = c(CRAN = "https://artifactory.gcp.anz/artifactory/r-project-cran/"))

options(download.file.method = "curl")
options(download.file.extra = "--insecure")

# Loop through the packages
for (i in seq_along(packages_to_install)) {
  package_name <- packages_to_install[i]
  
  # Check if the package is already installed
  if (!require(package_name, character.only = TRUE)) {
    # If not installed, install the package
    install.packages(package_name)
    
    # Check again if the installation was successful
    if (require(package_name, character.only = TRUE)) {
      cat(paste(i, ':', "Package", package_name, "installed successfully.\n"))
    } else {
      cat(paste(i, ':', "Failed to install package", package_name, "\n"))
    }
  } else {
    # If the package is already installed, print a message
    cat(paste(i, ':', "Package", package_name, "is already installed.\n"))
  }
}

devtools::install_github('GCM/gcm.ReferenceTables',host='https://github.service.anz/api/v3')