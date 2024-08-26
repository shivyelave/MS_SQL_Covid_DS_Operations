use covid_vaccine;

-- Query to select all records from the covid_19_india table.
select * from covid_19_india;

-- Query to select all records from the covid_vaccine_statewise table.
select * from covid_vaccine_statewise;

-- Query to select all records from the StatewiseTestingDetails table.
select * from StatewiseTestingDetails;

-- Using JOINS to combine the covid_deaths and covid_vaccine tables
-- 1. To find out the population vs the number of people vaccinated.

-- This query joins two tables: covid_vaccine_statewise and StatewiseTestingDetails,
-- It calculates the total population (approximated using TotalSamples from StatewiseTestingDetails)
-- and the total number of vaccinated individuals in each state.
select 
    covid_vaccine_statewise.State as state, 
    sum(cast(StatewiseTestingDetails.TotalSamples as float)) as population, 
    sum(cast(covid_vaccine_statewise.[Total Individuals Vaccinated] as float)) as vaccinated
from 
    covid_vaccine_statewise 
    INNER JOIN StatewiseTestingDetails 
    ON covid_vaccine_statewise.State = StatewiseTestingDetails.State
group by 
    covid_vaccine_statewise.State;

-- 2. To find out the percentage of different vaccines taken by people in a country.

-- First, delete records where the Total Doses Administered is zero, to clean the data.
delete from covid_vaccine_statewise
where cast([Total Doses Administered] as float) = 0;

-- Query to calculate the percentage of Covaxin, CoviShield, and Sputnik V vaccines administered
-- compared to the total number of doses administered. The results are grouped by the date 
-- when the data was updated.
select 
    [Updated On] as date,
    round(sum(cast([ Covaxin (Doses Administered)] as float)) / 
          (sum(cast([Total Doses Administered] as float))) * 100, 3) as Covaxin_Percentage, 
    round(sum(cast([CoviShield (Doses Administered)] as float)) / 
          (sum(cast([Total Doses Administered] as float))) * 100, 3) as Covishield_Percentage, 
    round(sum(cast([Sputnik V (Doses Administered)] as float)) / 
          (sum(cast([Total Doses Administered] as float))) * 100, 3) as Sputnik_V_Percentage
from 
    covid_vaccine_statewise
group by 
    [Updated On];

-- 3. To find out the percentage of people who took both doses.

-- This query calculates the percentage of people who took the second dose compared 
-- to the total doses administered.
select 
    round(sum(cast([Second Dose Administered] as float)) / 
          sum(cast([Total Doses Administered] as float)), 3) as Second_Dose_Percentage
from 
    covid_vaccine_statewise;
