CREATE TABLE IF NOT EXISTS `Users` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`name` varchar(80) NOT NULL CHECK (`name` <> ''),
	`address` varchar(200) NOT NULL CHECK (`address` <> ''),
	`phone` varchar(45) NOT NULL CHECK (`phone` <> ''),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Books` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`title` varchar(255) NOT NULL CHECK (`title` <> ''),
	`author` varchar(255) NOT NULL CHECK (`author` <> ''),
	`year` int NOT NULL,
	`genre` varchar(100) NOT NULL CHECK (`genre` <> ''),
	PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `Transactions` (
	`id` int AUTO_INCREMENT NOT NULL UNIQUE,
	`book_id` int NOT NULL,
	`user_id` int NOT NULL,
	`issue_date` date NOT NULL,
	`return_date` date,
	PRIMARY KEY (`id`)
);



ALTER TABLE `Transactions` ADD CONSTRAINT `Transactions_fk1` FOREIGN KEY (`user_id`) REFERENCES `Users`(`id`) ON DELETE CASCADE;

ALTER TABLE `Transactions` ADD CONSTRAINT `Transactions_fk2` FOREIGN KEY (`book_id`) REFERENCES `Books`(`id`) ON DELETE CASCADE;