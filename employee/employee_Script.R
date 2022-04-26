#Install Packages
install.packages("dplyr")
install.packages("data.table")
install.packages("reshape")
install.packages("reshape")

#Import Libraries
library(dplyr)
library(reshape)
library(hflights)
library(data.table)


#Get the data to df variable
df_employee<-read.csv("D:/Employee/Employee.csv")

head(df_employee)

df_interview<-read.csv("D:/Employee/Interview.csv")

head(df_interview)

df_resigned=read.csv("D:/Employee/ResignedEmployee.csv")
head(df_resigned)

#Get an idea about the columns in each csv
names(df_employee)
names(df_interview)
names(df_resigned)

#Get rough idea about three data frames
str(df_employee)
str(df_interview)
str(df_resigned)

#Get the idea on dimensions about each data frame
dim(df_employee)
dim(df_interview)
dim(df_resigned)

#Get an idea on number of rows and number of columns in each data frame
ncol(df_employee)
nrow(df_employee)

ncol(df_interview)
nrow(df_interview)

ncol(df_resigned)
nrow(df_resigned)
#.......................................................Data Cleaning...................................................................

#add column to df_resigned data frame
df_resigned$Resigned<-1

head(df_resigned)



#Remove unnecessary columns from the data frame which are not effect to the analysis
#From Employee data frame-Data frame manipulation
#Remove Date of birth column, since data is not recorded appropriately
drops <- c("DateOfBirth")
df_employee_1<-df_employee[ , !(names(df_employee) %in% drops)]
head(df_employee_1)

#From df_interview data frame NIC and Telephone number column have been removed since those are sensitive information.
#Interview gate and interview person has been removed since it is an unnessary parameter for analysis, this has been selected by domain knowledge.
#dateInterviewed,last working year and last working month, year joined apperal,year joined for apperal, experience duration years,experience duration years
#date join and year married denoted by Apperal experience column. Therfore these columns has been removed.
#permanat residence town has been denoted by permanant residence district in employee data frame.
drops <- c("YearJoinedApparel","DateInterviewed","LastWorkingYear","LastWorkingMonth","YearJoinedApparel","ExperienceDurationYears","ExperienceDurationMonths","PermanentResidenceTown","NIC","InterviewedBy","DateJoin","YearMarried","Telephone.Number","Interview.Gate")
df_interview_1<-df_interview[ , !(names(df_interview) %in% drops)]
head(df_interview_1)


#Get unique features in each column
print('Unique Features in Gender Column :')
df_employee_1[!duplicated(df_employee_1[,c('Gender')]),]

#There are two categories in gender column: Male, Female

print('Unique Features in PermanentResidenceDistrict Column :')
df_employee_1[!duplicated(df_employee_1[,c('PermanentResidenceDistrict')]),]
#The categories in PermanentResidenceDistrict column: Colombo, Gampaha,Matara,Hambantota,Ampara,Nuwara Eliya,Moneragala,Ratnapura,Badulla
#Anuradhapura,Galle,Kegalle,Kandy,Polonnaruwa,Kalutara,Matale,Kurunegala,Trincomalee,Puttalam,Jaffna,Vavuniya,Mullaitivu,Kilinochchi

print('Unique Features in Residence Column :')
df_employee_1[!duplicated(df_employee_1[,c('Residence')]),]
#The categories in Residence column:Coming From Home,Boarded,Coming From Relative's Place

print('Unique Features in CivilStatus Column :')
df_employee_1[!duplicated(df_employee_1[,c('CivilStatus')]),]
#The categories in CivilStatus column:Married,Single,Divorced,Widowed

print('Unique Features in HighestEducationalQualification Column :')
df_employee_1[!duplicated(df_employee_1[,c('HighestEducationalQualification')]),]
#The categories in HighestEducationalQualification column:have studied up to G.C.E O/L,have sat for G.C.E A/L, but haven?t got through A/L,
#haven?t sat for G.C.E O/L,'have got through G.C.E O/L but haven?t sat for G.C.E A/L',have passed G.C.E A/L and had no higher education,
#have got a university degree/ university diploma,have passed G.C.E A/L and waiting for university admission

#.....................................................................................................................................
#merge two data frames (df_interview, df_resigned)
new_merged<-merge(df_interview_1, df_resigned, by = c("ReferenceNumber","ID"),all.x = TRUE)
head(new_merged)

#Fill N/A values with 0
new_merged$Resigned[is.na(new_merged$Resigned)] <- 0
head(new_merged)

#Write this data frame to csv
write.csv(new_merged,"D:/Employee/MyData.csv", row.names = FALSE)

#merge two data frames (df_interview, df_resigned)
merged_per_res<-merge(df_employee_1, df_resigned, by = c("ReferenceNumber"),all.x = TRUE)
head(merged_per_res)
merged_per_res$Resigned[is.na(merged_per_res$Resigned)] <- 0

#Write this data frame to csv
write.csv(merged_per_res,"D:/Employee/MyData_2.csv", row.names = FALSE)
#......................................................................................................................................

#Now you have the two merged data frames
#new_merged- Resigned employees details and interview details
#merged_per_re-employee personal details and resigned or not details


#lets do some explontory data analysis using these two data frames
install.packages("ggplot2")
library(ggplot2)
#Order bar chart for resigned employees for gender wise
with(merged_per_res, table(Resigned, Gender))
ggplot(merged_per_res, aes(x = Gender, fill = Resigned)) + geom_bar()

#Order bar chart for resigned employees for PermanentResidenceDistrict wise
with(merged_per_res, table(Resigned, PermanentResidenceDistrict))
ggplot(merged_per_res, aes(x = PermanentResidenceDistrict, fill = Resigned)) + geom_bar(fill = "steelblue")

#............................................................................................................................
#get the number of rows in merged data frames
nrow(new_merged)
nrow(merged_per_res)

#..........................................................................................................................
new_merged<- data.frame(new_merged)

merged_per_res$Gender[which(merged_per_res$Gender == 'Female')] <- 1
merged_per_res$Gender[which(merged_per_res$Gender == 'Male')] <- 0

merged_per_res$Residence[which(merged_per_res$Residence == 'Coming From Home')] <- 0
merged_per_res$Residence[which(merged_per_res$Residence == 'Boarded')] <- 1
merged_per_res$Residence[which(merged_per_res$Residence == "Coming From Relative's Place")] <- 2

merged_per_res$CivilStatus[which(merged_per_res$CivilStatus == 'Single')] <- 0
merged_per_res$CivilStatus[which(merged_per_res$CivilStatus == 'Married')] <- 1
merged_per_res$CivilStatus[which(merged_per_res$CivilStatus == 'Widowed')] <- 2
merged_per_res$CivilStatus[which(merged_per_res$CivilStatus == 'Divorced')] <- 3

#...............................................................................................................................................
District_list=list('Colombo','Gampaha','Matara','Hambantota','Ampara','Nuwara Eliya','Moneragala','Ratnapura','Badulla','Anuradhapura','Galle','Kegalle','Kandy','Polonnaruwa','Kalutara','Matale','Kurunegala','Trincomalee','Puttalam','Jaffna','Vavuniya','Mullaitivu','Kilinochchi')

i=0
for (d in District_list){
  print (d)
  merged_per_res$PermanentResidenceDistrict[which(merged_per_res$PermanentResidenceDistrict == d)] <- i
  i=i+1
}

#..................................................................................................................................  
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'have studied up to G.C.E O/L')] <- 0
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'have sat for G.C.E A/L, but haven?t got through A/L')] <- 1
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'haven?t sat for G.C.E O/L')] <- 2
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'have got through G.C.E O/L but haven?t sat for G.C.E A/L')] <- 3
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'have passed G.C.E A/L and had no higher education')] <- 4
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'have got a university degree/ university diploma')] <- 5
merged_per_res$HighestEducationalQualification[which(merged_per_res$HighestEducationalQualification == 'have passed G.C.E A/L and waiting for university admission')] <- 6


write.csv(merged_per_res,"D:/Employee/Transformed_employee_data.csv", row.names = FALSE)
#.................................................................................................................................. 
#Convert new_merged data frame like this manner
#Find the columns in this data frame
names(new_merged)

#Recognize the continuous variables and catergorical variables in this data frame by observation
#Continuous variables- Weight.Kg,Height.cm.,IQTestScore
#Catergorical variables-ApparelRelatedVocationalQualification,RelativesInApparel,Referel,Selection,PersonalImpression,SelectedDepartment,ApparelExperience,Weight.Kg and rest all variables are continuous.
#The values in these variables should be denoted in numeric values.
#To do that first identify the unique values in each catergorical columns and replace them with numerical values

new_merged[!duplicated(new_merged[,c('ApparelRelatedVocationalQualification')]),]

new_merged$ApparelRelatedVocationalQualification[which(new_merged$ApparelRelatedVocationalQualification == 'FALSE')] <- 0
new_merged$ApparelRelatedVocationalQualification[which(new_merged$ApparelRelatedVocationalQualification == 'TRUE')] <- 1
#..................................................................................................................................

new_merged[!duplicated(new_merged[,c('ExtraCurricularActivities')]),]

new_merged$ExtraCurricularActivities[which(new_merged$ExtraCurricularActivities == 'FALSE')] <- 0
new_merged$ExtraCurricularActivities[which(new_merged$ExtraCurricularActivities == 'TRUE')] <- 1
#..................................................................................................................................

new_merged[!duplicated(new_merged[,c('PreviousJob')]),]

new_merged$PreviousJob[which(new_merged$PreviousJob == 'No Job')] <- 0
new_merged$PreviousJob[which(new_merged$PreviousJob == 'Apparel')] <- 1
new_merged$PreviousJob[which(new_merged$PreviousJob == 'Non Apparel')] <- 2
#.................................................................................................................................
new_merged[!duplicated(new_merged[,c('ExperienceSection')]),]

Expreince_list=list('Packing','Other','SMO','Helper','Cutting','Knitting','Maintenance','Checking')

i=1
for (d in Expreince_list){
  print (d)
  new_merged$ExperienceSection[which(new_merged$ExperienceSection == d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('RelativesInApparel')]),]

response_list=list('FALSE','TRUE')

i=0
for (d in response_list){
  print (d)
  new_merged$RelativesInApparel[which(new_merged$RelativesInApparel == d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('SpousesOccupation')]),]

response_list=list('Government Employee','Working In A Privet Company/Factory','Have No Job','No Permanent Job','Self Employee','Disabled')

i=1
for (d in response_list){
  print (d)
  new_merged$SpousesOccupation[which(new_merged$SpousesOccupation == d)] <- i
  i=i+1
  
}
#.................................................................................................................................
new_merged[!duplicated(new_merged[,c('FamilyOpinionAboutTheJob')]),]

response_list=list("Don't Like",'Like')

i=0
for (d in response_list){
  print (d)
  new_merged$FamilyOpinionAboutTheJob[which(new_merged$FamilyOpinionAboutTheJob == d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('Referel')]),]

response_list=list('Leaflets/Posters/Banners','Friend','Relative','Other','Announcement')

i=0
for (d in response_list){
  print (d)
  new_merged$Referel[which(new_merged$Referel == d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('ExpectationOfDoingTheJob')]),]

response_list=list('Like a career in Apparel','To financially support family','No specific reason','To fulfill a specific short term objective ( education, settle a loan, wedding)')

i=0
for (d in response_list){
  print (d)
  new_merged$ExpectationOfDoingTheJob[which(new_merged$ExpectationOfDoingTheJob == d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('AvailabilityOfTransportNearTheResidence')]),]

response_list=list('No','Yes')

i=0
for (d in response_list){
  print (d)
  new_merged$AvailabilityOfTransportNearTheResidence[which(new_merged$AvailabilityOfTransportNearTheResidence == d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('Selection')]),]

response_list=list('No','Yes','Pending')

i=0
for (d in response_list){
  print (d)
  new_merged$Selection[which(new_merged$Selection == d)] <- i
  i=i+1
  
}
#.................................................................................................................................


new_merged[!duplicated(new_merged[,c('ReasonForChoosingApparel')]),]

response_list=list('Like Sewing','Other','Family members are working in Apparel',"Couldn't find another job","Close Proximity to home")

i=0
for (d in response_list){
  print (d)
  new_merged$ReasonForChoosingApparel[which(new_merged$ReasonForChoosingApparel == d)] <- i
  i=i+1
  
}
#.................................................................................................................................


new_merged[!duplicated(new_merged[,c('ContributionToTheFamilyIncome')]),]

response_list=list('No Contribution','High Contribution','Moderate Contribution',"Total Contribution","Less Contribution")

i=0
for (d in response_list){
  print (d)
  new_merged$ContributionToTheFamilyIncome[which(new_merged$ContributionToTheFamilyIncome== d)] <- i
  i=i+1
  
}
#.................................................................................................................................


new_merged[!duplicated(new_merged[,c('PersonalImpression')]),]

response_list=list('Bad','Average','Good')

i=0
for (d in response_list){
  print (d)
  new_merged$PersonalImpression[which(new_merged$PersonalImpression== d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('AccommodationFee')]),]

response_list=list('1500/= or Less than 1500/=','Over 1500/= and 3000/= or below','Over 3000/= and 4500/= or below','Over 4500/= and 6000/= or below',' Over 6000/=')

i=1
for (d in response_list){
  print (d)
  new_merged$AccommodationFee[which(new_merged$AccommodationFee== d)] <- i
  i=i+1
  
}
#.................................................................................................................................


new_merged[!duplicated(new_merged[,c('RetentionCategory')]),]

response_list=list('A','B','C','D')

i=1
for (d in response_list){
  print (d)
  new_merged$RetentionCategory[which(new_merged$RetentionCategory== d)] <- i
  i=i+1
  
}
#.................................................................................................................................


new_merged[!duplicated(new_merged[,c('SelectedDepartment')]),]

response_list=list('TM (Checker)','TM (MO)','TM (HS)','TM (Packing)','TM (SA)')

i=1
for (d in response_list){
  print (d)
  new_merged$SelectedDepartment[which(new_merged$SelectedDepartment== d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('ApparelExperience')]),]

response_list=list('FALSE','TRUE')

i=0
for (d in response_list){
  print (d)
  new_merged$ApparelExperience[which(new_merged$ApparelExperience== d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('ReasonForLeaving')]),]

response_list=list('Other','Overseas Job','Work-Life Balance Issue','Not a Satisfied Salary','Travelling Issue','Maternity','Work Load/High Stress','No Career Progression','Marriage','Changing the residence')

i=1
for (d in response_list){
  print (d)
  new_merged$ReasonForLeaving[which(new_merged$ReasonForLeaving== d)] <- i
  i=i+1
  
}
#.................................................................................................................................

new_merged[!duplicated(new_merged[,c('MedicalTest')]),]

response_list=list('Failed','Passed')

i=0
for (d in response_list){
  print (d)
  new_merged$MedicalTest[which(new_merged$MedicalTest== d)] <- i
  i=i+1
  
}
#.................................................................................................................................
new_merged[!duplicated(new_merged[,c('FollowingExternalCourses')]),]

response_list=list('No','Expect','Yes')

i=0
for (d in response_list){
  print (d)
  new_merged$FollowingExternalCourses[which(new_merged$FollowingExternalCourses== d)] <- i
  i=i+1
  
}
#.................................................................................................................................
#Rejection reason and reason for leaving both reflects the same impression. Reason for quit the job opportunity.Therefore, decided to drop the Rejection reason column 
#since it provide same reason repetitively.And PRT column also dropped.It consists of the name of the interviewer.
 
drops <- c("PRT","RejectionReason")
new_merged_1<-new_merged[ , !(names(new_merged) %in% drops)]
head(new_merged_1)


write.csv(new_merged_1,"D:/Employee/Transformed_interview_data.csv", row.names = FALSE)

#.................................................................................................................................
#The new_merged_1 data set consists of details of interviwers who got selected and not selected both.But we want to get the details of people who get selected and 
#quit the job. Therefore we can delete the rows which selection column==0 and pending value==2.

new_merged_2<-new_merged_1[!(new_merged_1$Selection=="0"),]
new_merged_3<-new_merged_2[!(new_merged_2$Selection=="2"),]

#ensure whther all unnessary rows are removed or not
nrow(new_merged_3)
new_merged_3[!duplicated(new_merged_3[,c('Selection')]),]

write.csv(new_merged_3,"D:/Employee/Transformed_interview_data_2.csv", row.names = FALSE)

#........................................................Recognizing and replacing missing Values......................................................
#Find missing values in merged_per_res data frame
names(merged_per_res)

sum(is.na(merged_per_res))
#There are 2594 N/A values is in this data frame. Find these values are in which columns.
sum(is.na(merged_per_res$Gender))
sum(is.na(merged_per_res$PermanentResidenceDistrict))
sum(is.na(merged_per_res$Residence))
sum(is.na(merged_per_res$CivilStatus))
sum(is.na(merged_per_res$HighestEducationalQualification))
sum(is.na(merged_per_res$ID))

#All the N/A values are in the ID column.Since there is an another column for participant recognition we can remove this column.
drops <- c("ID")
merged_per_res_1<-merged_per_res[ , !(names(merged_per_res) %in% drops)]
head(merged_per_res_1)

#Find whther there is an any empty rows in this data set
merged_per_res_1$Gender[merged_per_res_1$Gender == ""] <- NA
merged_per_res_1$PermanentResidenceDistrict[merged_per_res_1$PermanentResidenceDistrict == ""] <- NA
merged_per_res_1$Residence[merged_per_res_1$Residence == ""] <- NA
merged_per_res_1$CivilStatus[merged_per_res_1$CivilStatus == ""] <- NA
merged_per_res_1$HighestEducationalQualification[merged_per_res_1$HighestEducationalQualification == ""] <- NA

sum(is.na(merged_per_res_1$Gender))
sum(is.na(merged_per_res_1$PermanentResidenceDistrict))
sum(is.na(merged_per_res_1$Residence))
sum(is.na(merged_per_res_1$CivilStatus))
sum(is.na(merged_per_res_1$HighestEducationalQualification))

sum(is.na(merged_per_res_1$ReferenceNumber))

#Now merged_per_res_1 data frame is with no missing data.
write.csv(merged_per_res_1,"D:/Employee/Transformed_employee_data_nomissing.csv", row.names = FALSE)

#.................................................................................................................................
#Find empty and missing values in new_merged_3 data frame
#First we find whther we have columns with N/A values
names(new_merged_3)

sum(is.na(new_merged_3$ExtraCurricularActivities))
sum(is.na(new_merged_3$ApparelRelatedVocationalQualification))
sum(is.na(new_merged_3$PreviousJob))
sum(is.na(new_merged_3$ExperienceSection))
sum(is.na(new_merged_3$RelativesInApparel))
sum(is.na(new_merged_3$SpousesOccupation))
sum(is.na(new_merged_3$FamilyOpinionAboutTheJob))
sum(is.na(new_merged_3$Referel))
sum(is.na(new_merged_3$ExpectationOfDoingTheJob))
sum(is.na(new_merged_3$AvailabilityOfTransportNearTheResidence))
sum(is.na(new_merged_3$ReasonForChoosingApparel))
sum(is.na(new_merged_3$ContributionToTheFamilyIncome))
sum(is.na(new_merged_3$PersonalImpression))
sum(is.na(new_merged_3$AccommodationFee))
sum(is.na(new_merged_3$RetentionCategory))
sum(is.na(new_merged_3$SelectedDepartment))
sum(is.na(new_merged_3$ChildrenLessThan5Years))
sum(is.na(new_merged_3$NumberOfChildren))
sum(is.na(new_merged_3$ApparelExperience))
sum(is.na(new_merged_3$ReasonForLeaving))
sum(is.na(new_merged_3$Height.cm))
sum(is.na(new_merged_3$Weight.Kg.))
sum(is.na(new_merged_3$MedicalTest))
sum(is.na(new_merged_3$IQTestScore))
sum(is.na(new_merged_3$LastBasicSalary))
sum(is.na(new_merged_3$FollowingExternalCourses))
sum(is.na(new_merged_3$Resigned))

#There are three columns with N/A Values-ChildrenLessThan5Years,NumberOfChildren,LastBasicSalary
#If there is no previous job, there is no last basic salary, Therefore we have consider it.
df_NopreviousJob<-new_merged_3[is.na(new_merged_3$LastBasicSalary),] 
write.csv(df_NopreviousJob,"D:/Employee/NopreviousJob.csv", row.names = FALSE)

#According to these results Last basic salary data is missing the people who have worked before as well.
#Therefore we can fill these details with mean value of salary. But sometimes they have not given details or they may work in unpaid jobs or daily wages.
#Since these data is not accurate. it can be assumed that NA values in last basic salary column as zero.replace all NA values in zero.
new_merged_3$LastBasicSalary[is.na(new_merged_3$LastBasicSalary)]<-0

#.................................................................................................................................
#In here there are 67 missing values in weight column.To each person have a Weight.Therefore it can be replaced by a value.The missing values replaced by column mean value
new_merged_3$Weight.Kg.[is.na(new_merged_3$Weight.Kg.)] <- mean(new_merged_3$Weight.Kg., na.rm = TRUE)

#Ensure whther is there any missing values in this data set weight column
sum(is.na(new_merged_3$Weight.Kg.))

#.................................................................................................................................
#There are two other columns with missing values are ChildrenLessThan5Years and NumberOfChildren columns,Sometimes these columns have missing values since they are not married.
#To observe that we have to merge the both data frames new_merged_3 and merged_per_res_1. Before merging these two data frames first we find are there any columns with empty values
#in new_merged_3 data frame.
new_merged_3$ExtraCurricularActivities[new_merged_3$ExtraCurricularActivities == ""] <- NA
new_merged_3$ApparelRelatedVocationalQualification[new_merged_3$ApparelRelatedVocationalQualification == ""] <- NA
new_merged_3$PreviousJob[new_merged_3$PreviousJob == ""] <- NA
new_merged_3$ExperienceSection[new_merged_3$ExperienceSection == ""] <- NA
new_merged_3$RelativesInApparel[new_merged_3$RelativesInApparel == ""] <- NA
new_merged_3$SpousesOccupation[new_merged_3$SpousesOccupation == ""] <- NA
new_merged_3$FamilyOpinionAboutTheJob[new_merged_3$FamilyOpinionAboutTheJob == ""] <- NA
new_merged_3$Referel[new_merged_3$Referel == ""] <- NA
new_merged_3$ExpectationOfDoingTheJob[new_merged_3$ExpectationOfDoingTheJob == ""] <- NA
new_merged_3$AvailabilityOfTransportNearTheResidence[new_merged_3$AvailabilityOfTransportNearTheResidence == ""] <- NA
new_merged_3$ReasonForChoosingApparel[new_merged_3$ReasonForChoosingApparel == ""] <- NA
new_merged_3$ContributionToTheFamilyIncome[new_merged_3$ContributionToTheFamilyIncome == ""] <- NA
new_merged_3$PersonalImpression[new_merged_3$PersonalImpression == ""] <- NA
new_merged_3$AccommodationFee[new_merged_3$AccommodationFee == ""] <- NA
new_merged_3$RetentionCategory[new_merged_3$RetentionCategory == ""] <- NA
new_merged_3$SelectedDepartmente[new_merged_3$SelectedDepartment == ""] <- NA
new_merged_3$ApparelExperience[new_merged_3$ApparelExperience == ""] <- NA
new_merged_3$ReasonForLeaving[new_merged_3$ReasonForLeaving == ""] <- NA
new_merged_3$Height.cm[new_merged_3$Height.cm == ""] <- NA
new_merged_3$MedicalTest[new_merged_3$MedicalTest == ""] <- NA
new_merged_3$IQTestScore[new_merged_3$IQTestScore == ""] <- NA
new_merged_3$FollowingExternalCourses[new_merged_3$FollowingExternalCourses == ""] <- NA
new_merged_3$Resigned[new_merged_3$Resigned == ""] <- NA



sum(is.na(new_merged_3$ExtraCurricularActivities))
sum(is.na(new_merged_3$ApparelRelatedVocationalQualification))
sum(is.na(new_merged_3$PreviousJob))
sum(is.na(new_merged_3$ExperienceSection))
sum(is.na(new_merged_3$RelativesInApparel))
sum(is.na(new_merged_3$SpousesOccupation))
sum(is.na(new_merged_3$FamilyOpinionAboutTheJob))
sum(is.na(new_merged_3$Referel))
sum(is.na(new_merged_3$ExpectationOfDoingTheJob))
sum(is.na(new_merged_3$AvailabilityOfTransportNearTheResidence))
sum(is.na(new_merged_3$ReasonForChoosingApparel))
sum(is.na(new_merged_3$ContributionToTheFamilyIncome))
sum(is.na(new_merged_3$PersonalImpression))
sum(is.na(new_merged_3$AccommodationFee))
sum(is.na(new_merged_3$RetentionCategory))
sum(is.na(new_merged_3$SelectedDepartment))

sum(is.na(new_merged_3$ApparelExperience))
sum(is.na(new_merged_3$ReasonForLeaving))
sum(is.na(new_merged_3$Height.cm))

sum(is.na(new_merged_3$MedicalTest))
sum(is.na(new_merged_3$IQTestScore))

sum(is.na(new_merged_3$FollowingExternalCourses))
sum(is.na(new_merged_3$Resigned))



#According to this results it can be concluded that AccommodationFee,ReasonForLeaving,SpousesOccupation,ExperienceSection columns have missing values. All these columns are catergorical
#variables. 
#First consider on experience section,it may be not applicable since these participants have no prior experience, or since this is their first job.
#Check whther their previous job section have values with 0 or two.
df_NopreviousJob<-new_merged_3[is.na(new_merged_3$ExperienceSection),] 
write.csv(df_NopreviousJob,"D:/Employee/NopreviousExperience.csv", row.names = FALSE)

sum(df_NopreviousJob$PreviousJob==1)

#.......................................................................................................................................

#This shows that the people who worked before in the apperal industry have not answered to this question.ExperienceSection has catergory called other which denotes number 2.
#Therfore all the empty values will be filled by number 2
new_merged_3$ExperienceSection[is.na(new_merged_3$ExperienceSection)]<-2

sum(is.na(new_merged_3$ExperienceSection))

#............................................................................................................................................
#reason for leaving column.If they not resigned, this column is not applicable. In that case we put 0 and if not put 1 for other reson catergory

if (new_merged_3$Resigned==1){
  new_merged_3$ReasonForLeaving[is.na(new_merged_3$ReasonForLeaving)]<-1
}else{
  new_merged_3$ReasonForLeaving[is.na(new_merged_3$ReasonForLeaving)]<-0
}

sum(is.na(new_merged_3$ReasonForLeaving))

#............................................................................................................................................

#SpouseOccupation- All missing values because of husband died or divorced or actually her husband has no job or value missing.
#Therefore we will assume all missing data reflects no job value. Repalce all N/As with have no Job option number 3.
new_merged_3$SpousesOccupation[is.na(new_merged_3$SpousesOccupation)]<-3

sum(is.na(new_merged_3$SpousesOccupation))

write.csv(new_merged_3,"D:/Employee/new_merged_3.csv", row.names = FALSE)
names(new_merged_3)
new_merged_4<-new_merged_3
new_merged_5<-new_merged_4[, -c(31:32)]
names(new_merged_5)
#............................................................................................................................................

#AccommodationFee column also has missing values- it has following catergories
#1500/= or Less than 1500/=','Over 1500/= and 3000/= or below','Over 3000/= and 4500/= or below','Over 4500/= and 6000/= or below',' Over 6000/='
#If participant coming from her/his own home there is no accomodation fee.
#therefore we have to first find it. To find it we have to merge the other data frame as well.
#............................................................................................................................................

#.................................................merging two data frames-new_merged_3 and merged_per_res_1....................................
#left side data frame-new_merged_3and viseversa
Analysis_df<-merge(new_merged_5,merged_per_res_1,by=c("ReferenceNumber"),all.x = TRUE)

head(Analysis_df)
names(Analysis_df)

#drop ID and REsigned.y Columns
drops <- c("ID","Resigned.y","Selection")

Analysis_df_new<-Analysis_df[,!(names(Analysis_df)%in%drops)]
write.csv(Analysis_df_new,"D:/Employee/Analysis_df.csv", row.names = FALSE)


#............................................................................................................................................

#Replace missing values in number of children column
names(Analysis_df_new)
mean(Analysis_df_new$NumberOfChildren, na.rm = TRUE)


if (Analysis_df_new$CivilStatus==0 &is.na(Analysis_df_new$NumberOfChildren)){
  Analysis_df_new$NumberOfChildren[is.na(Analysis_df_new$NumberOfChildren)]<-0
}else{
  Analysis_df_new$NumberOfChildren[is.na(Analysis_df_new$NumberOfChildren)]<-1
}

sum(is.na(Analysis_df_new$NumberOfChildren))

#............................................................................................................................................
#Replace missing values in ChildrenLessThan5Years column
mean(Analysis_df_new$ChildrenLessThan5Years, na.rm = TRUE)


if (Analysis_df_new$NumberOfChildren==0 &is.na(Analysis_df_new$ChildrenLessThan5Years)){
  Analysis_df_new$ChildrenLessThan5Years[is.na(Analysis_df_new$ChildrenLessThan5Years)]<-0
}else{
  Analysis_df_new$ChildrenLessThan5Years[is.na(Analysis_df_new$ChildrenLessThan5Years)]<-0
}

sum(is.na(Analysis_df_new$ChildrenLessThan5Years))
#...........................................................................................................................................
#Replace missing values in AccommodationFee column
mean(Analysis_df_new$AccommodationFee, na.rm = TRUE)

sapply(Analysis_df_new$AccommodationFee, typeof)
Analysis_df_new$AccommodationFee <- as.numeric(as.character(Analysis_df_new$AccommodationFee))
sapply(Analysis_df_new$AccommodationFee, typeof)
mean(Analysis_df_new$AccommodationFee, na.rm = TRUE)

if (Analysis_df_new$Residence==1 &is.na(Analysis_df_new$AccommodationFee)){
  Analysis_df_new$AccommodationFee[is.na(Analysis_df_new$AccommodationFee)]<-3
}else{
  Analysis_df_new$AccommodationFee[is.na(Analysis_df_new$AccommodationFee)]<-0
}

sum(is.na(Analysis_df_new$AccommodationFee))
#...........................................................................................................................................

#To move on to a further analysis, we need to convert all columns in data frame from character, string to numeric types.
#First find the character type column and convert them to numeric types
sapply(Analysis_df_new, typeof)

#character types columns are PreviousJob,ExperienceSection,SpousesOccupation,FamilyOpinionAboutTheJob,Referel,ExpectationOfDoingTheJob,AvailabilityOfTransportNearTheResidence,
#ReasonForChoosingApparel,ContributionToTheFamilyIncome,PersonalImpression,RetentionCategory,SelectedDepartment,ReasonForLeaving,MedicalTest,IQTestScore,FollowingExternalCourses,
#Gender,PermanentResidenceDistrict,Residence,CivilStatus,HighestEducationalQualification 


Analysis_df_new$PreviousJob <- as.numeric(as.character(Analysis_df_new$PreviousJob))
Analysis_df_new$ExperienceSection <- as.numeric(as.character(Analysis_df_new$ExperienceSection))
Analysis_df_new$SpousesOccupation <- as.numeric(as.character(Analysis_df_new$SpousesOccupation))
Analysis_df_new$FamilyOpinionAboutTheJob <- as.numeric(as.character(Analysis_df_new$FamilyOpinionAboutTheJob))
Analysis_df_new$Referel <- as.numeric(as.character(Analysis_df_new$Referel))
Analysis_df_new$ExpectationOfDoingTheJob <- as.numeric(as.character(Analysis_df_new$ExpectationOfDoingTheJob))
Analysis_df_new$AvailabilityOfTransportNearTheResidence <- as.numeric(as.character(Analysis_df_new$AvailabilityOfTransportNearTheResidence))
Analysis_df_new$ReasonForChoosingApparel <- as.numeric(as.character(Analysis_df_new$ReasonForChoosingApparel))
Analysis_df_new$ContributionToTheFamilyIncome <- as.numeric(as.character(Analysis_df_new$ContributionToTheFamilyIncome))
Analysis_df_new$PersonalImpression <- as.numeric(as.character(Analysis_df_new$PersonalImpression))
Analysis_df_new$RetentionCategory <- as.numeric(as.character(Analysis_df_new$RetentionCategory))
Analysis_df_new$SelectedDepartment <- as.numeric(as.character(Analysis_df_new$SelectedDepartment))
Analysis_df_new$ReasonForLeaving <- as.numeric(as.character(Analysis_df_new$ReasonForLeaving))
Analysis_df_new$MedicalTest <- as.numeric(as.character(Analysis_df_new$MedicalTest))
Analysis_df_new$IQTestScore <- as.numeric(as.character(Analysis_df_new$IQTestScore))
Analysis_df_new$FollowingExternalCourses <- as.numeric(as.character(Analysis_df_new$FollowingExternalCourses))
Analysis_df_new$Gender <- as.numeric(as.character(Analysis_df_new$Gender))
Analysis_df_new$PermanentResidenceDistrict <- as.numeric(as.character(Analysis_df_new$PermanentResidenceDistrict))
Analysis_df_new$Residence <- as.numeric(as.character(Analysis_df_new$Residence))
Analysis_df_new$CivilStatus <- as.numeric(as.character(Analysis_df_new$CivilStatus))
Analysis_df_new$HighestEducationalQualification <- as.numeric(as.character(Analysis_df_new$HighestEducationalQualification))

Analysis_df_new$IQTestScore[is.na(Analysis_df_new$IQTestScore)]<-mean(Analysis_df_new$IQTestScore, na.rm = TRUE)
sum(is.na(Analysis_df_new$IQTestScore))
Analysis_df_new$IQTestScore <- as.numeric(as.character(Analysis_df_new$IQTestScore))
sapply(Analysis_df_new, typeof)

#...........................................................................................................................................
#............................................Descriptive Statistics..........................................................
#We can use Analysis_df_ed data frame for analysis and ML model development
ncol(Analysis_df_new)
nrow(Analysis_df_new)

dim(Analysis_df_new)

summary(Analysis_df_new)
#...........................................................................................................................................
#But here we can see still data type of selected department is not changed. Therefore we have to change the data type of this column and there are 1 NA values in some columns
#First we change it.
Analysis_df_new_1<-Analysis_df_new

df_one<-Analysis_df_new_1[!is.na(Analysis_df_new_1$Gender), ]


summary(df_one)
write.csv(Analysis_df_new,"D:/Employee/df_one.csv", row.names = FALSE)

#...........................................................................................................................................
#Finding outliers
names(df_one)

#We can detect outliers in a data frame column using various methods
#Box_plot Visualization
#Follow statistical tests-Grubbs’s test,Dixon’s test,Rosner’s test
#But this data set consisits of both catergorical and continuous variables as well. Therefore we can use HDoutlier package to detect
#outlier in a data set with continuos and catergorical variables both.
install.packages("HDoutliers")
library(HDoutliers)

out.W<-HDoutliers(df_one[,-1])
plotHDoutliers(df_one[,-1], out.W)


#According to the graph, Which produces the following output where no outliers appear (outliers are denoted by an asterisk rather than a blue point)
#Therefore no need of outlier imputation

#...........................................................................................................................................
#Normalization of data
#since we are going to develop a machine learning model it is important to standerdize the data.
#If we don't normalize the data, the machine learning algorithm will be dominated by the variables that use a larger scale, 
#adversely affecting model performance. This makes it imperative to normalize the data.
#First we have to recognize the continuous variables are normally distributed or not.
#The continuous varaibles in this data set is ChildrenLessThan5Years,"NumberOfChildren,Height.cm.,Weight.Kg.,IQTestScore,LastBasicSalary
#using shapiro.test() check whther data is normally distributed or not

shapiro.test(df_one$ChildrenLessThan5Years)

#From the output, the p-value < 0.05 implying that the distribution of the data are significantly different from normal distribution.
#Further the data is not normally distributed

shapiro.test(df_one$NumberOfChildren)
#From the output, the p-value < 0.05 implying that the distribution of the data are significantly different from normal distribution.
#Further the data is not normally distributed

shapiro.test(df_one$Height.cm.)
#From the output, the p-value < 0.05 implying that the distribution of the data are significantly different from normal distribution.
#Further the data is not normally distributed

shapiro.test(df_one$Weight.Kg.)
#From the output, the p-value < 0.05 implying that the distribution of the data are significantly different from normal distribution.
#Further the data is not normally distributed

shapiro.test(df_one$IQTestScore)
#From the output, the p-value < 0.05 implying that the distribution of the data are significantly different from normal distribution.
#Further the data is not normally distributed

shapiro.test(df_one$LastBasicSalary)
#From the output, the p-value < 0.05 implying that the distribution of the data are significantly different from normal distribution.
#Further the data is not normally distributed

#..................................................................................................................................

#Therefore, it should be need to do standerdization
#Since this data set is not consists any outliers ,we use standerdization method.
#Standardization is a technique in which all the features are centred around zero and have roughly unit variance.
install.packages("caret")
library(caret)

names(df_one)
preproc1 <- preProcess(df_one[,c(17:18,21:22,24:25)], method=c("center", "scale"))

norm1 <- predict(preproc1, df_one[,c(17:18,21:22,24:25)])

summary(norm1)

#..................................................................................................................................
#merge df_resigned data frame to this data frame again to better results
drops <- c("Resigned.x")

df_new<-df_one[,!(names(df_one)%in%drops)]

names(df_new)

df_ed<-merge(df_new,df_resigned,by=c("ReferenceNumber"),all.x = TRUE)
names(df_ed)

drops <- c("ID")

df_ed_1<-df_ed[,!(names(df_ed)%in%drops)]

sum(is.na(df_ed_1$Resigned))
dim(df_ed_1)

df_ed_1$Resigned[is.na(df_ed_1$Resigned)]<-0
sapply(df_ed_1$Resigned, typeof)

sum(df_ed_1$Resigned==1.0)
sum(df_ed_1$Resigned==0.0)

write.csv(df_ed_1,"D:/Employee/df_ed_1.csv", row.names = FALSE)

df_ed_2<-df_ed_1


#.........................................DATA CLEANING AND DATA WRANGLING PART IS OVER.............................................................

#.........................................................DATA PREPARATION.........................................................................
#original data set should be seperated as train and test data set
#will split data frame into train(70%) and test(30%)
install.packages("dplyr")
library(dplyr)

train_df<-sample_frac(df_ed_2, 0.7)
sid<-as.numeric(rownames(train_df)) # because rownames() returns character
test_df<-df_ed_2[-sid,]

#get the shape of each data frames
dim(train_df)
dim(test_df)

names(train_df)
X_train<-train_df[0:31]
names(X_train)
dim(X_train)
Y_train<-train_df['Resigned']
dim(Y_train)

names(test_df)
X_test<-test_df[0:31]
names(X_test)
dim(X_test)
Y_test<-test_df['Resigned']
dim(Y_test)

#To check whther we can apply classification model or regression model
sum(train_df$Resigned==1.0)
sum(train_df$Resigned==0.0)

sum(test_df$Resigned==1.0)
sum(test_df$Resigned==0.0)



#We can see target catergorical variable divided according to 57:1823 ratio in training data set and 36:770 ration in test data set.
#here highest number of participants produce the results as not-resigned. therefore results is biased to this side. This is an error in sampling method.


#...........................................Machine Learning Model Development..................................................................
#In here we can apply both regression and classification models and find a best fitted model with high accuracy.

#Regression models- traditional linear regression model, Stepwise liner regression model
#Classification Models- Random Forest, Desicion Tree,
#But our aim is to find whther employee is reteined or not. To predict which class employee with some specific parameters belongs to.
#Therefore classification techniques are better than regression techniques.


#Model object creation and train the model
install.packages("caret")
library(caret)


install.packages("randomForest")
library(randomForest)

install.packages("mlbench")
library(mlbench)

install.packages("e1071")
library(e1071)


rf <- randomForest(Resigned~.,data = train_df)

set.seed(7)
control <- trainControl(method="repeatedcv", number=10, repeats=3)
fit.rf <- train(train_df$Resigned~.,data = X_train, method="rf", metric="Accuracy", trControl=control, ntree=2000)
print(fit.rf)
print(fit.rf$finalModel)

#Since Random Forest model is not successful try to fit logistic regression
install.packages("aod")
library(aod)

train_df$Resigned <- factor(train_df$Resigned)
mylogit <- glm(Resigned ~ ., data = train_df, family = "binomial")
summary(mylogit)

#Fit the same model after removing referenceNumber column
drops <- c("ReferenceNumber")

train_df<-train_df[,!(names(train_df)%in%drops)]
test_df<-test_df[,!(names(test_df)%in%drops)]

train_df$Resigned <- factor(train_df$Resigned)
mylogit <- glm(Resigned ~ ., data = train_df, family = "binomial")
summary(mylogit)

## CIs using profiled log-likelihood
confint(mylogit)

## CIs using standard errors
confint.default(mylogit)

#Model Evaluation
#To get the effect of each level in other catergorical variables
wald.test(b = coef(mylogit), Sigma = vcov(mylogit), Terms = 4:6)
wald.test(b = coef(mylogit), Sigma = vcov(mylogit), Terms = 2:3)
wald.test(b = coef(mylogit), Sigma = vcov(mylogit), Terms = 6:9)

## odds ratios only
exp(coef(mylogit))

#Prediction
newdata1 <- with(train_df, data.frame(test_df))

## view data frame with predicted values
newdata1

newdata1$preResigned <- predict(mylogit, newdata = newdata1, type = "response")
newdata1


#It can be concluded that the predicted values are close to actual values and fitted model is the correct model to describe the behaviour of these data.
