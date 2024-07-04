-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-5.7
-- Время создания: Июл 04 2024 г., 13:38
-- Версия сервера: 5.7.44
-- Версия PHP: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `documents`
--

-- --------------------------------------------------------

--
-- Структура таблицы `Contracts`
--

CREATE TABLE `Contracts` (
  `contract_id` int(11) NOT NULL,
  `contract_number` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contract_date` date DEFAULT NULL,
  `contract_subject_id` int(11) DEFAULT NULL,
  `contract_amount` decimal(10,2) DEFAULT NULL,
  `contract_currency_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `ContractSubjects`
--

CREATE TABLE `ContractSubjects` (
  `subject_id` int(11) NOT NULL,
  `subject_description` text COLLATE utf8mb4_unicode_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Currency`
--

CREATE TABLE `Currency` (
  `currency_id` int(11) NOT NULL,
  `currency_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Parties`
--

CREATE TABLE `Parties` (
  `party_id` int(11) NOT NULL,
  `party_name` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `party_type` enum('Partner','Supplier','Buyer','Official') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `party_signature` tinyint(1) DEFAULT NULL,
  `party_stamp` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Signatures`
--

CREATE TABLE `Signatures` (
  `signature_id` int(11) NOT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `party_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `Stamps`
--

CREATE TABLE `Stamps` (
  `stamp_id` int(11) NOT NULL,
  `contract_id` int(11) DEFAULT NULL,
  `party_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `Contracts`
--
ALTER TABLE `Contracts`
  ADD PRIMARY KEY (`contract_id`),
  ADD KEY `contract_subject_id` (`contract_subject_id`),
  ADD KEY `contract_currency_id` (`contract_currency_id`);

--
-- Индексы таблицы `ContractSubjects`
--
ALTER TABLE `ContractSubjects`
  ADD PRIMARY KEY (`subject_id`);

--
-- Индексы таблицы `Currency`
--
ALTER TABLE `Currency`
  ADD PRIMARY KEY (`currency_id`);

--
-- Индексы таблицы `Parties`
--
ALTER TABLE `Parties`
  ADD PRIMARY KEY (`party_id`);

--
-- Индексы таблицы `Signatures`
--
ALTER TABLE `Signatures`
  ADD PRIMARY KEY (`signature_id`),
  ADD KEY `contract_id` (`contract_id`),
  ADD KEY `party_id` (`party_id`);

--
-- Индексы таблицы `Stamps`
--
ALTER TABLE `Stamps`
  ADD PRIMARY KEY (`stamp_id`),
  ADD KEY `contract_id` (`contract_id`),
  ADD KEY `party_id` (`party_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `Contracts`
--
ALTER TABLE `Contracts`
  MODIFY `contract_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `ContractSubjects`
--
ALTER TABLE `ContractSubjects`
  MODIFY `subject_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Currency`
--
ALTER TABLE `Currency`
  MODIFY `currency_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Parties`
--
ALTER TABLE `Parties`
  MODIFY `party_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Signatures`
--
ALTER TABLE `Signatures`
  MODIFY `signature_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `Stamps`
--
ALTER TABLE `Stamps`
  MODIFY `stamp_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `Contracts`
--
ALTER TABLE `Contracts`
  ADD CONSTRAINT `contracts_ibfk_1` FOREIGN KEY (`contract_subject_id`) REFERENCES `ContractSubjects` (`subject_id`),
  ADD CONSTRAINT `contracts_ibfk_2` FOREIGN KEY (`contract_currency_id`) REFERENCES `Currency` (`currency_id`);

--
-- Ограничения внешнего ключа таблицы `Signatures`
--
ALTER TABLE `Signatures`
  ADD CONSTRAINT `signatures_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `Contracts` (`contract_id`),
  ADD CONSTRAINT `signatures_ibfk_2` FOREIGN KEY (`party_id`) REFERENCES `Parties` (`party_id`);

--
-- Ограничения внешнего ключа таблицы `Stamps`
--
ALTER TABLE `Stamps`
  ADD CONSTRAINT `stamps_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `Contracts` (`contract_id`),
  ADD CONSTRAINT `stamps_ibfk_2` FOREIGN KEY (`party_id`) REFERENCES `Parties` (`party_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
