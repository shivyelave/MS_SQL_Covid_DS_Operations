use covid_datasets;

select * from country_wise_latest;
select * from covid_19_clean_complete;
select * from day_wise;
select * from full_grouped;
select * from usa_county_wise;
select * from worldometer_data;

-- 1. To find out the death percentage locally and globally

select [Country Region] , round(sum(cast(Deaths as float))/sum(cast(Confirmed as float))* 100 ,2) as Death_Percent
from country_wise_latest 
group by [Country Region]
order by [Country Region];

select round(sum(cast(Deaths as float))/sum(cast(Confirmed as float))* 100 ,2) as Global_Death_Percent
from country_wise_latest 
;


-- 2. To find out the infected population percentage locally and globally

select Population from worldometer_data
where Population = 0

delete from worldometer_data
where Population = 0;

select [Country Region] , round(sum(cast(TotalCases as float))/sum(cast(Population as float))* 100 ,2) as Infected_Percent
from worldometer_data 
group by [Country Region]
order by [Country Region];

select round(sum(cast(TotalCases as float))/sum(cast(Population as float))* 100 ,2) as Global_Infected_Percent
from worldometer_data; 
;

-- 3. To find out the countries with the highest infection rates

select top(100) [Country Region] ,  round(sum(cast(TotalCases as float))/sum(cast(Population as float)) ,4) as Infected_Peoples
from worldometer_data 
group by [Country Region]
order by [Infected_Peoples] DESC;

--4. To find out the countries and continents with the highest death counts

select [Country Region] , sum(cast(TotalDeaths as float)) as Total_Deaths
from worldometer_data 
group by [Country Region]
order by Total_Deaths DESC;

select Continent , sum(cast(TotalDeaths as float)) as Total_Deaths
from worldometer_data 
group by Continent
order by Total_Deaths DESC;

-- 5. Average number of deaths by day (Continents and Countries)

SELECT 
    [Country Region], 
    AVG(Daily_Total_Deaths) AS Average_Daily_Deaths
FROM (
    -- Calculate the total number of deaths per day and per country or region
    SELECT 
        [Country Region],
        Date,
        SUM(CAST(Deaths AS FLOAT)) AS Daily_Total_Deaths
    FROM 
        full_grouped
    GROUP BY 
        [Country Region],
        Date
) AS Daily_Deaths
GROUP BY 
    [Country Region]
ORDER BY 
    Average_Daily_Deaths DESC;


SELECT 
    [WHO Region], 
    AVG(Daily_Total_Deaths) AS Average_Daily_Deaths
FROM (
    -- Calculate the total number of deaths per day and per country or region
    SELECT 
        [WHO Region],
        Date,
        SUM(CAST(Deaths AS FLOAT)) AS Daily_Total_Deaths
    FROM 
        full_grouped
    GROUP BY 
        [WHO Region],
        Date
) AS Daily_Deaths
GROUP BY 
    [WHO Region]
ORDER BY 
    Average_Daily_Deaths DESC;


-- 6. Average of cases divided by the number of population of each country (TOP 10) 

select top(10) [Country Region] ,  round(sum(cast(TotalCases as float))/sum(cast(Population as float)) ,4) as Infected_AVG
from worldometer_data 
group by [Country Region]
order by Infected_AVG DESC;

-- 7. Considering the highest value of total cases, which countries have the highest rate of infection in relation to population? 

select top(1) [Country Region] ,  round(sum(cast(TotalCases as float))/sum(cast(Population as float)) ,4) as Infected_AVG
from worldometer_data 
group by [Country Region]
order by Infected_AVG DESC;