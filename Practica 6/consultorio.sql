drop database if exists Consultorio;
create database Consultorio;
use Consultorio;

CREATE TABLE `admin` (
    `ID` INT NOT NULL AUTO_INCREMENT,
    `RFC` VARCHAR(50) NOT NULL,
    `Nombre` VARCHAR(50) NOT NULL,
    `Apellidopa` VARCHAR(50) NOT NULL,
    `Apellidoma` VARCHAR(50) NOT NULL,
    `Cedula` VARCHAR(50) NOT NULL,
    `Correo` VARCHAR(50) NOT NULL,
    `Rol` VARCHAR(50) NOT NULL,
    `Contraseña` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`ID`)
);

CREATE TABLE `registro_paciente` (
    `Id_paciente` INT NOT NULL AUTO_INCREMENT,
    `Medico_id` INT NOT NULL,
    `Nombre` VARCHAR(50) NOT NULL,
    `Apellidopa` VARCHAR(50) NOT NULL,
    `Apellidoma` VARCHAR(50) NOT NULL,
    `Fecha_nacimiento` VARCHAR(50) NOT NULL,
    `Enfermedades` VARCHAR(50),
    `Alergias` VARCHAR(50),
    `Antecedentes_familiares` VARCHAR(50),
    PRIMARY KEY (`Id_paciente`),
    FOREIGN KEY (`Medico_id`) REFERENCES `admin`(`ID`)
);


CREATE TABLE `exploracion_diagnostico` (
    `Id_exp` INT NOT NULL AUTO_INCREMENT,
    `Id_paciente` INT NOT NULL,
    `Fecha` VARCHAR(50) NOT NULL,
    `Peso` VARCHAR(50) NOT NULL,
    `Altura` VARCHAR(50) NOT NULL,
    `Temperatura` VARCHAR(50) NOT NULL,
    `Latidos` VARCHAR(50) NOT NULL,
    `Oxigeno` VARCHAR(50) NOT NULL,
    `Edad` VARCHAR(50) NOT NULL,
    `Sintomas` VARCHAR(50) NOT NULL,
    `DX` VARCHAR(50) NOT NULL,
    `Tratamiento` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`Id_exp`),
    FOREIGN KEY (`Id_paciente`) REFERENCES `registro_paciente`(`Id_paciente`)
);



CREATE TABLE `cita` (
    `Id_cita` INT NOT NULL AUTO_INCREMENT,
    `Fecha_cita` VARCHAR(50) NOT NULL,
    `Id_exp` INT NOT NULL,
    PRIMARY KEY (`Id_cita`),
    FOREIGN KEY (`Id_exp`) REFERENCES `exploracion_diagnostico`(`Id_exp`)
);

insert into `admin` (`RFC`, `Nombre`, `Apellidopa`, `Apellidoma`, `Cedula`, `Correo`, `Rol`, `Contraseña`)
values ('RACP010525ABC', 'Pablo', 'Ramírez', 'Carrillo', '123456789', '019032786@upq.edu.mx', 'Administrador', 'contraseña123'),
 ('ABC123', 'Juan', 'Pérez', 'González', '98467345', 'juan@example.com', 'Medico', 'password123'),
 ('DEF456', 'María', 'López', 'García', '09278436', 'maria@example.com', 'Medico', 'securepass');
select * from admin;
select * from registro_paciente;
select * from exploracion_diagnostico;