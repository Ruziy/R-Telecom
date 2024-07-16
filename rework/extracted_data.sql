-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: MySQL-5.7
-- Время создания: Июл 16 2024 г., 22:45
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
-- База данных: `pdf_data`
--

-- --------------------------------------------------------

--
-- Структура таблицы `extracted_data`
--

CREATE TABLE `extracted_data` (
  `id` int(11) NOT NULL,
  `document_number` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `contract_date` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `first_party` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `second_party` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `first_details` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `second_details` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stamps_present` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Дамп данных таблицы `extracted_data`
--

INSERT INTO `extracted_data` (`id`, `document_number`, `contract_date`, `first_party`, `second_party`, `amount`, `first_details`, `second_details`, `stamps_present`) VALUES
(1, NULL, '2024', 'Ссфьа _лексеевна Ютян', 'Неврасов', '500000р', 'отделон !ФмС в Caмape', 'этлал__MСв_Capaнсье', 1),
(20, NULL, '2024', 'Ссфьа _лексеевна Ютян', 'Неврасов', '500000р', 'отделон !ФмС в Caмape', 'этлал__MСв_Capaнсье', 1),
(21, NULL, '2024', 'Цылин_Даннла Игоревн', 'Нвзнов Нван Иванов:', 'ЗООООР', 'отделоч УФМС Россин _Cavaрa', 'отделон ~Ф]С Россишн ЕЕкзтеринб_г', 0),
(22, NULL, '2024', 'Цылин_Даннла Игоревн', 'Нвзнов Нван Иванов:', 'ЗООООР', 'отделоч УФМС Россин _Cavaрa', 'отделон ~Ф]С Россишн ЕЕкзтеринб_г', 0),
(23, NULL, '2024', 'Ссфьа _лексеевна Ютян', 'Неврасов', '500000р', 'отделон !ФмС в Caмape', 'этлал__MСв_Capaнсье', 1),
(24, NULL, '2024', 'Ссфьа _лексеевна Ютян', 'Неврасов', '500000р', 'отделон !ФмС в Caмape', 'этлал__MСв_Capaнсье', 1),
(25, NULL, '2024', 'Цылиин _анила Кгоревие', 'Иванов Иван Иванов ', '300000р', 'отделон !ФмС Росстн I Caiapа', 'этлал__Kа_Воссн_EEr=винSшP5', 1);

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `extracted_data`
--
ALTER TABLE `extracted_data`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `extracted_data`
--
ALTER TABLE `extracted_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
