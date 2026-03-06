drop table if exists WaterSource cascade;
drop table if exists Cataclysms cascade;
drop table if exists Observations cascade;
drop table if exists Person cascade;
drop table if exists FoodSource cascade;
drop table if exists LifeFormDistribution cascade;
drop table if exists LifeForm cascade;
drop table if exists NaturalZoneDistribution cascade;
drop table if exists Planet cascade;
drop table if exists HeatSource cascade;
drop table if exists NaturalZone cascade;
drop table if exists Resource cascade;
drop table if exists ResourceDistribution cascade;

drop type if exists water_source_type cascade;
drop type if exists food_source_type cascade;
drop type if exists life_form_type cascade;
drop type if exists planet_type cascade;
drop type if exists heat_source_type cascade;
drop type if exists natural_zone_type cascade;
drop type if exists sizes cascade;
drop type if exists resource_type cascade;

create type natural_zone_type as enum ('Forest', 'Desert', 'Tundra', 'Grassland', 'Mountain');

create type resource_type as enum ('Salt', 'Iron', 'Gas', 'Gold');

create type heat_source_type as enum ('Geothermal', 'Solar', 'Volcanic', 'Artificial');

create type planet_type as enum ('Terrestrial', 'Gas Giant', 'Ice Giant', 'Satellite');

create type life_form_type as enum ('Human', 'Animal', 'Plant', 'Microorganism', 'Alien');

create type food_source_type as enum ('Herbivore', 'Carnivore', 'Omnivore', 'Photosynthesis');

create type water_source_type as enum ('River', 'Lake', 'Ocean', 'Underground');

create type sizes as enum ('Small', 'Medium', 'Large', 'Huge');


begin;

-- стержневые
create table NaturalZone (
    id SERIAL primary key,
    name VARCHAR(255) not null ,
    type natural_zone_type,
    size sizes
);

create table Planet (
    id SERIAL primary key,
    name VARCHAR(255) not null ,
    type planet_type,
    size sizes
);

create table LifeForm (
    id SERIAL primary key,
    name VARCHAR(255) not null ,
    type life_form_type
);

create table Person (
    id SERIAL primary key,
    name VARCHAR(255) not null,
    height INTEGER,
    weight INTEGER,
    age INTEGER check (age>=18)
);

create table Resource (
	id SERIAL primary key,
	name VARCHAR(255) not null,
	type resource_type
); 

-- 1 to many (характеристические)
create table HeatSource(
	id SERIAL primary key,
	type heat_source_type not null,
	heat_level INTEGER default 1,
	natural_zone_id INTEGER references NaturalZone(id)
);

create table Cataclysms (
    id SERIAL primary key,
    name VARCHAR(255) not null,
    natural_zone_id INTEGER references NaturalZone(id),
    date DATE
);

create table WaterSource (
    id SERIAL primary key,
    natural_zone_id INTEGER references NaturalZone(id),
    type water_source_type,
    name VARCHAR(255) not null
);

create table FoodSource (
    id SERIAL primary key,
    name VARCHAR(255) not null,
    life_form_id INTEGER references LifeForm(id),
    type food_source_type,
    satiety INTEGER default 0
);

-- many to many (Ассоциативные)
create table LifeFormDistribution (
    life_form_id INTEGER not null references LifeForm(id),
    natural_zone_id INTEGER not null references NaturalZone(id),
    primary key (life_form_id, natural_zone_id)
);

create table Observations (
    person_id INTEGER not null references Person(id),
    planet_id INTEGER not null references Planet(id),
    date timestamp,
    primary key (person_id, planet_id, date)
);

create table NaturalZoneDistribution (
    planet_id INTEGER not null references Planet(id),
    natural_zone_id INTEGER not null references NaturalZone(id),
    primary key (planet_id, natural_zone_id)
);


create table ResourceDistribution (
	natural_zone_id INTEGER not null references NaturalZone(id),
	resource_id INTEGER not null references Resource(id),
	primary key (natural_zone_id, resource_id)
);



insert into NaturalZone (name, type, size) 
values 
    ('Amazon Rainforest', 'Forest', 'Large'),
    ('Sahara Desert', 'Desert', 'Huge'),
    ('Arctic Tundra', 'Tundra', 'Medium');

insert into Planet (name, type, size) 
values 
    ('Earth', 'Terrestrial', 'Medium'),
    ('Jupiter', 'Gas Giant', 'Huge'),
    ('Mars', 'Terrestrial', 'Small'),
	('Io', 'Satellite', 'Small'),
	('Europe', 'Satellite', 'Small');

insert into Resource (name, type)
values 
	('Mineral salt', 'Salt'),
	('Magnetit', 'Iron');



insert into LifeForm (name, type) 
values 
    ('Person', 'Human'),
    ('Lion', 'Animal'),
    ('Oak Tree', 'Plant');

insert into Person (name, height, weight, age) 
values 
    ('John Doe', 180, 75, null),
    ('Jane Smith', 165, 60, null);

insert into HeatSource (type, heat_level) 
values 
    ('Geothermal', 5),
    ('Solar', 10);

insert into Cataclysms (name, natural_zone_id, date) 
values 
    ('Earthquake', 1, '2153-01-15'),
    ('Sandstorm', 2, '2197-02-20');

insert into WaterSource (natural_zone_id, type, name) 
values 
    (3, 'River', 'Amazon River'),
    (2, 'Lake', 'Chad Lake'),
	(1, 'Ocean', 'Ocean Depths');

insert into FoodSource (name, life_form_id, type, satiety) 
values 
    ('Grass', 3, 'Photosynthesis', 5),
    ('Meat', 2, 'Carnivore', 10);

insert into LifeFormDistribution (life_form_id, natural_zone_id) 
values 
    (1, 1),
    (2, 2),
    (3, 1);

insert into Observations (person_id, planet_id, date) 
values 
    (1, 1, '2012-03-01'),
    (2, 3, '2013-03-01');

insert into NaturalZoneDistribution (planet_id, natural_zone_id) 
values 
    (1, 1),
    (1, 2),
    (3, 3);

insert into ResourceDistribution (natural_zone_id, resource_id)
values
	(1, 1),
	(1, 2);


create or replace function check_ecological_balance()
returns trigger as $$
DECLARE
    current_lifeforms INTEGER;
    zone_type natural_zone_type;
    max_lifeforms INTEGER;
BEGIN 

    SELECT type INTO zone_type FROM NaturalZone
    WHERE id = NEW.natural_zone_id;
    
    CASE zone_type
        WHEN 'Forest' THEN max_lifeforms := 20;
        WHEN 'Desert' THEN max_lifeforms := 10;
        WHEN 'Tundra' THEN max_lifeforms := 15;
        WHEN 'Grassland' THEN max_lifeforms := 25;
        WHEN 'Mountain' THEN max_lifeforms := 18;
        ELSE max_lifeforms := 15;
    END CASE;
    

    SELECT COUNT(*) INTO current_lifeforms 
    FROM LifeFormDistribution 
    WHERE natural_zone_id = NEW.natural_zone_id;
    
    IF current_lifeforms > max_lifeforms THEN
        RAISE EXCEPTION 'Экологическая катастрофа! В зоне % уже максимальное количество форм жизни (%)', 
                        zone_type, max_lifeforms;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER ecological_balance_lifeform
BEFORE INSERT OR UPDATE ON LifeFormDistribution
FOR EACH ROW EXECUTE FUNCTION check_ecological_balance();
