-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-12-2022 a las 06:32:31
-- Versión del servidor: 10.4.20-MariaDB
-- Versión de PHP: 7.3.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `librarydb`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `autors`
--

CREATE TABLE `autors` (
  `idAutors` int(11) NOT NULL,
  `nameAutors` varchar(60) NOT NULL,
  `lsnameAutors` varchar(60) NOT NULL,
  `bibliography` varchar(350) NOT NULL,
  `yoldAutors` int(11) NOT NULL,
  `dateAutors` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `statusAutors` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `autors`
--

INSERT INTO `autors` (`idAutors`, `nameAutors`, `lsnameAutors`, `bibliography`, `yoldAutors`, `dateAutors`, `statusAutors`) VALUES
(1, 'Gabriel', 'García Márquez', 'Gabriel José de la Concordia García Márquez fue un escritor y periodista colombiano. Reconocido principalmente por sus novelas y cuentos, también escribió narrativa de no ficción, discursos, reportajes, críticas cinematográficas y memorias. Fue conocido como Gabo, y familiarmente y por sus amigos como Gabito.', 78, '2022-12-22 18:31:58', NULL),
(3, 'Edgar', 'Allan Poe', 'Edgar Allan Poe fue un escritor, poeta, crítico y periodista romántico estadounidense, generalmente reconocido como uno de los maestros universales del relato corto, del cual fue uno de los primeros practicantes en su país. Fue renovador de la novela gótica, recordado especialmente por sus cuentos de terror.', 189, '2022-12-25 20:15:05', NULL),
(4, 'Jane', 'Austen', 'Jane Austen (Steventon, 16 de diciembre de 1775-Winchester, 18 de julio de 1817) fue una novelista británica que vivió durante la época georgiana. La ironía que empleaba para dotar de comicidad a sus novelas hace que Jane Austen sea considerada entre los clásicos de la novela inglesa, a la vez que su recepción va, incluso en la actualidad, más allá', 300, '2022-12-25 20:05:42', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `books`
--

CREATE TABLE `books` (
  `idBooks` int(11) NOT NULL,
  `nameBooks` varchar(100) NOT NULL,
  `frontBooks` varchar(200) DEFAULT NULL,
  `descriptions` varchar(250) NOT NULL,
  `priceBooks` decimal(11,2) NOT NULL,
  `dateBooks` timestamp NOT NULL DEFAULT current_timestamp(),
  `statusBooks` varchar(10) DEFAULT NULL,
  `idAutors` int(11) NOT NULL,
  `idGeners` int(11) NOT NULL,
  `idEditorials` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `car`
--

CREATE TABLE `car` (
  `idCar` int(11) NOT NULL,
  `idBooks` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `editorials`
--

CREATE TABLE `editorials` (
  `idEditorials` int(11) NOT NULL,
  `nameEditorials` varchar(70) NOT NULL,
  `dateEditorials` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `editorials`
--

INSERT INTO `editorials` (`idEditorials`, `nameEditorials`, `dateEditorials`) VALUES
(4, 'Editorial de prueba', '2022-12-27 01:00:40'),
(5, 'Otra editorial', '2022-12-27 01:00:40'),
(6, 'Editorial para la vida', '2022-12-27 01:00:40'),
(7, 'Editorial?', '2022-12-27 01:00:40'),
(8, 'MM.. Editorial', '2022-12-27 01:00:40'),
(9, 'Quieres una editorial?', '2022-12-27 01:00:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `geners`
--

CREATE TABLE `geners` (
  `idGeners` int(11) NOT NULL,
  `nameGeners` varchar(20) NOT NULL,
  `dateGeners` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `geners`
--

INSERT INTO `geners` (`idGeners`, `nameGeners`, `dateGeners`) VALUES
(1, 'Terror', '2022-12-25 21:57:00'),
(2, 'Slayer', '2022-12-25 21:57:09'),
(3, 'Siencia Ficción', '2022-12-25 21:57:25'),
(4, 'Documental', '2022-12-25 22:01:08'),
(5, 'Acción', '2022-12-25 22:01:23'),
(6, 'Medieval', '2022-12-25 22:01:49');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `idRol` int(11) NOT NULL,
  `nameRol` varchar(70) NOT NULL,
  `dateRol` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`idRol`, `nameRol`, `dateRol`) VALUES
(1, 'Administrator', '2022-12-21 23:53:31'),
(2, 'Employee', '2022-12-21 23:53:31'),
(3, 'Buyer', '2022-12-21 23:53:31'),
(4, 'Fireman', '2022-12-22 06:35:04'),
(12, 'Police', '2022-12-25 20:06:32');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `idUsers` int(11) NOT NULL,
  `nameUsers` varchar(15) NOT NULL,
  `passUsers` varchar(20) NOT NULL,
  `dateUsers` timestamp NOT NULL DEFAULT current_timestamp(),
  `idRol` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`idUsers`, `nameUsers`, `passUsers`, `dateUsers`, `idRol`) VALUES
(1, 'Admin', '123', '2022-12-22 00:32:54', 1),
(2, 'Employee', '123', '2022-12-22 00:32:54', 2),
(3, 'Buyer', '123', '2022-12-22 00:32:54', 3),
(4, 'Joseph123', '54321', '2022-12-22 03:23:55', 1),
(5, 'Minion123', '06112022', '2022-12-22 03:42:21', 1),
(6, 'Paty0099', '33425435', '2022-12-22 03:44:09', 2),
(10, 'Michael Myers', '3110000', '2022-12-24 20:09:43', 3),
(31, 'Panda8983', '12345', '2022-12-25 17:42:53', 3),
(32, 'Julieth34', '23558', '2022-12-25 19:21:58', 3),
(33, 'Nath3pr', '23558', '2022-12-25 20:03:40', 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `autors`
--
ALTER TABLE `autors`
  ADD PRIMARY KEY (`idAutors`);

--
-- Indices de la tabla `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`idBooks`),
  ADD KEY `idAutors` (`idAutors`),
  ADD KEY `idGeners` (`idGeners`),
  ADD KEY `idEditorials` (`idEditorials`);

--
-- Indices de la tabla `car`
--
ALTER TABLE `car`
  ADD PRIMARY KEY (`idCar`),
  ADD KEY `idBooks` (`idBooks`);

--
-- Indices de la tabla `editorials`
--
ALTER TABLE `editorials`
  ADD PRIMARY KEY (`idEditorials`);

--
-- Indices de la tabla `geners`
--
ALTER TABLE `geners`
  ADD PRIMARY KEY (`idGeners`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`idRol`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`idUsers`),
  ADD KEY `idRol` (`idRol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `autors`
--
ALTER TABLE `autors`
  MODIFY `idAutors` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `car`
--
ALTER TABLE `car`
  MODIFY `idCar` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `editorials`
--
ALTER TABLE `editorials`
  MODIFY `idEditorials` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `geners`
--
ALTER TABLE `geners`
  MODIFY `idGeners` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `idRol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `idUsers` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`idAutors`) REFERENCES `autors` (`idAutors`) ON DELETE CASCADE,
  ADD CONSTRAINT `books_ibfk_2` FOREIGN KEY (`idGeners`) REFERENCES `geners` (`idGeners`) ON DELETE CASCADE,
  ADD CONSTRAINT `books_ibfk_3` FOREIGN KEY (`idEditorials`) REFERENCES `editorials` (`idEditorials`) ON DELETE CASCADE;

--
-- Filtros para la tabla `car`
--
ALTER TABLE `car`
  ADD CONSTRAINT `car_ibfk_1` FOREIGN KEY (`idBooks`) REFERENCES `books` (`idBooks`) ON DELETE CASCADE;

--
-- Filtros para la tabla `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`idRol`) REFERENCES `rol` (`idRol`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
