DROP DATABASE IF EXISTS blsQcew;
CREATE DATABASE blsQcew;
USE blsQcew;

CREATE TABLE combined_quarters(
    id INT,
    own_code VARCHAR(10) REFERENCES own_titles(own_code),
    industry_code VARCHAR(10) REFERENCES industry_titles(industry_code),
    agglvl_code VARCHAR(10) REFERENCES agglvl_titles(agglvl_code),
    year INT,
    qtr INT,
    disclosure_code VARCHAR(5),
    qtrly_estabs INT,
    month1_emplvl INT,
    month2_emplvl INT,
    month3_emplvl INT,
    total_qtrly_wages BIGINT,
    avg_wkly_wage INT,
    PRIMARY KEY (id)
);

CREATE TABLE combined_annuals(
    id INT,
    own_code VARCHAR(10) REFERENCES own_titles(own_code),
    industry_code VARCHAR(10) REFERENCES industry_titles(industry_code),
    agglvl_code VARCHAR(10) REFERENCES agglvl_titles(agglvl_code),
    year INT,
    disclosure_code VARCHAR(5),
    annual_avg_estabs INT,
    annual_avg_emplvl INT,
    annual_avg_wkly_wage INT,
    avg_annual_pay INT,
    PRIMARY KEY (id)
);

CREATE TABLE own_titles (
    own_code VARCHAR(10),
    own_title VARCHAR(80),
    PRIMARY KEY (own_code)
);

CREATE TABLE industry_titles(
    industry_code VARCHAR(10),
    industry_title VARCHAR(200),
    PRIMARY KEY (industry_code)
);

CREATE TABLE agglvl_titles (
    agglvl_code VARCHAR(10),
    agglvl_title VARCHAR(80),
    PRIMARY KEY (agglvl_code)
);
