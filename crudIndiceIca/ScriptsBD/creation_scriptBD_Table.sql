create database Ica;
use Ica;
create table variables_ica(Id bigint not null primary key,
oxigenoDisuelto decimal not null,
constraint chkOD check(oxigenoDisuelto >0.0),
solidosSuspendidosT decimal not null,
constraint chkSST check(solidosSuspendidosT >0.0),
demandaQuiOxigeno decimal not null,
constraint chkDQO check(demandaQuiOxigeno >0.0),
conductividadElectrica decimal not null,
constraint chkConduct check(conductividadElectrica > 0.0),
pH int not null,
indiceCalidad decimal not null,
calidadAgua varchar(12) not null,
sennalAlerta varchar(12) not null,
constraint calidadAguaCheck check(calidadAgua IN('Muy mala','Mala','Regular','Aceptable','Buena')),
constraint sennalAlertaCheck check(sennalAlerta IN('Rojo','Naranja','Amarillo','Verde','Azul'))
);

