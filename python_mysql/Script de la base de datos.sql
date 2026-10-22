create database clientesdb;
use clientesdb;
create table usuarios (
id int auto_increment primary key not null,
nombres varchar(50),
apellidos varchar(50),
sexo varchar(20),
telefono varchar(10)
)

select * from usuarios;
insert into usuarios values (null, "Erik", "Jarquin", "Masculino");
delete from usuarios where id = 2;

delete from usuarios where usuarios.id = 5;

update usuarios set usuarios.nombres = "Azucena", usuarios.apellidos = "Hernandez", usuarios.sexo = "Femenino" where usuarios.id = 4;