install.packages('tidyverse')
library(tidyverse)

# Main data source : https://datatopics.worldbank.org/world-development-indicators/

# read data containing country Names
countryData <- readr::read_delim('data/Country.csv', delim=';')

countryData %>%
  # remove space from column names
  dplyr::select_all(~gsub("\\s+|\\.", "_", .)) %>%
  # select countries and remove sub-continental regions (these regions have no currencies)
  dplyr::filter(!is.na(Currency_Unit)) %>%
  dplyr::arrange(Table_Name)-> Country


# read data containing heads of state for all countries
readr::read_csv('data/HeadsOfState.csv') %>%
  # remove space from column names
  dplyr::select_all(~gsub("\\s+|\\.", "_", .)) %>%
  dplyr::select(-c(1)) -> headsState

# read data containing female head of states
readr::read_csv('data/FemaleHeadOfState.csv') %>%
  dplyr::mutate(Gender="Female") %>%
  dplyr::select(c(1,5)) -> femaleHeads


# Join heads of state data with data containing female headers of state to get Gender Info
headsState %>%
  dplyr::left_join(femaleHeads, by=c("State"="country")) %>%
  dplyr::mutate(Gender=ifelse(is.na(Gender), "Male", Gender)) %>%
  dplyr::rename(Gender_HoS=Gender) -> HeadsOfState

# Merge with main country data
Country %>%
  dplyr::left_join(HeadsOfState, by=c("Table_Name"="State")) %>%
  dplyr::select(!c(5, 9)) %>%
  dplyr::mutate(Head_of_state=ifelse(is.na(Head_of_state), "Information Missing", Head_of_state),
                Head_of_government=ifelse(is.na(Head_of_government), "Information Missing", Head_of_government),
                Gender_HoS=ifelse(is.na(Gender_HoS), "Information Missing", Gender_HoS)) -> FinalCountry


# Get complete data
readr::read_delim('data/CountryData.csv', delim=';') %>%
  dplyr::select_all(~gsub("\\s+|\\.", "_", .)) %>%
  dplyr::inner_join(FinalCountry, by=c("Country_Code"="Country_Code")) -> FinalCompleteData


# save data
write_delim(FinalCompleteData, "data/FinalCompleteData.csv")
