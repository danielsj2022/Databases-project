create table user(id int primary key auto_increment, uname varchar(45) not null, password varchar(200) not null);
create table music(sname varchar(100) primary key, date int, genre varchar(100), artist varchar(150), album varchar(150));
create table artist(aname varchar(150) primary key, agenre varchar(100), numalb int);

create table likes(id int, mname varchar(100), foreign key (id) references user(id), foreign key (mname) references music(sname), Primary key(id, mname));
create table listen_to(id int, aname varchar(150), foreign key (id) references user(id), foreign key (aname) references artist(aname), primary key(id, aname));
create table writes(sname varchar(100), aname varchar(150), foreign key (sname) references music(sname), foreign key (aname) references artist(aname), primary key(sname, aname));

create table part_group(aname varchar(150) primary key, gname varchar(150), foreign key (aname) references artist(aname));