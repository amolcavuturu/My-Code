#Set working Directory: example --> Bhavcopies for Feb 2019
setwd('D:/Investment Resources/zOthers/Scripts/Trades/Derivatives Bhavcopy/FO bhavcopies/2020/Feb')

#Define start and end dates
startDate = as.Date("2020-02-01", order="ymd")
endDate = as.Date("2020-02-28", order="ymd")



#Define date and filename variables
myDate = startDate
zippedFile <- tempfile()

#start the loop for all dates

while (myDate <= endDate){
  filenameDate = paste(as.character(myDate, "%y%m%d"), ".csv", sep = "")
  downloadfilename=paste("fo", toupper(as.character(myDate, "%d%b%Y")), "bhav.csv", sep = "")
  temp =""
                       
                       
                       
  #Define the url from where the file is to be extracted
  myURL = paste("https://www1.nseindia.com/content/historical/DERIVATIVES/", as.character(myDate, "%Y"),"/",toupper(as.character(myDate, "%b")),"/", downloadfilename, ".zip", sep = "")
                                                                                                                 
  #For missing dates, do a error catch check before you download the file
  tryCatch({download.file(myURL,zippedFile, method ="auto", quiet=FALSE)
  #unzip file and save it in temp
  temp <- read.csv(unzip(zippedFile), sep = ",")
  }, error=function(err){} )
 #Move to the next date
 myDate <- myDate+1
}

tryCatch()
  
  
  