create database if not exists inmatecensusdb;

grant usage on inmatecensusdb.* to censususer identified by 'password123%%%';

grant all privileges on inmatecensusdb.* to censususer;

use inmatecensusdb;

create table if not exists scraperruns(
scraperrunid int not null auto_increment primary key,
rundt datetime not null,
newdatafound boolean not null,
success boolean not null,
filename varchar(256) not null,
inmatecount int not null,
bookingscount int not null,
newinmates int not null
);

create index scraperruns_scraperrunid on scraperruns(scraperrunid);

create table if not exists inmates(
inmateid int not null auto_increment primary key,
first varchar(256) not null,
last varchar(256) not null,
middle varchar(256) not null,
mcid varchar(256) not null,
sex varchar(256) not null,
race varchar(256) not null,
dob date not null
);

create index inmates_inmateid on inmates(inmateid);
create index inmates_mcid on inmates(mcid);
create index inmates_sex on inmates(sex);
create index inmates_race on inmates(race);

create table if not exists custodies(
custodyid int not null auto_increment primary key,
inmateid int not null,
foreign key (inmateid) references inmates(inmateid),
custodydate date not null,
custodytime time not null,
custodyclass varchar(256) not null
);

create index custodies_custodyid on custodies(custodyid);

create table if not exists judges(
judgeid int not null auto_increment primary key,
fullname varchar(256) not null,
first varchar(256),
middle varchar(256),
last varchar(256)
);

create index judges_judgeid on judges(judgeid);

create table if not exists courts(
courtid int not null auto_increment primary key,
shortname varchar(256) not null,
fullname varchar(256),
description text
);

create index courts_courtid on courts(courtid);

create table if not exists arrestingagencies(
arrestingagencyid int not null auto_increment primary key,
fullname varchar(256) not null,
description text
);

create index arrestingagencies_arrestingagencyid on arrestingagencies(arrestingagencyid);

create table if not exists arresttypes(
arresttypeid int not null auto_increment primary key,
fullname varchar(256) not null,
description text
);

create index arresttypes_arrestttype on arresttypes(arresttypeid);

create table if not exists charges(
chargeid int not null auto_increment primary key,
fullname int not null,
description text
);

create index charges_chargeid on charges(chargeid);

create table if not exists bookings(
bookingid int not null auto_increment primary key,
inmateid int not null,
foreign key (inmateid) references inmates(inmateid),
censusdate date not null,
scraperrunid int not null,
foreign key (scraperrunid) references scraperruns(scraperrunid),
bookdatetime datetime not null,
booktype varchar(256) not null,
custodytype varchar(256) not null,
bail decimal not null,
bond decimal not null,
court varchar(256) not null,
courtid int not null,
foreign key (courtid) references courts(courtid),
judge varchar(256) not null,
judgeid int not null,
foreign key (judgeid) references judges(judgeid),
arrestingagency varchar(256) not null,
arrestingagencyid int not null,
foreign key (arrestingagencyid) references arrestingagencies(arrestingagencyid),
arresttype varchar(256) not null,
roc varchar(256) not null,
charge varchar(256) not null,
chargeid int not null,
foreign key (chargeid) references charges(chargeid),
indict varchar(256) not null,
adjusteddate date not null,
term varchar(256) not null
);

create index bookings_bookingid on bookings(bookingid);
create index bookings_booktype on bookings(booktype);
create index bookings_custodytype on bookings(custodytype);
create index bookings_court on bookings(court);
create index bookings_arresttype on bookings(arresttype);
create index bookings_indict on bookings(indict);

