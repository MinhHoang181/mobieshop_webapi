-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 05, 2021 at 08:29 AM
-- Server version: 5.7.32
-- PHP Version: 7.4.12

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `mobileshop`
--

-- --------------------------------------------------------

--
-- Table structure for table `actions`
--

CREATE TABLE `actions` (
  `action_id` int(11) NOT NULL,
  `action_name` varchar(100) NOT NULL,
  `action_detail` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `actions`
--

INSERT INTO `actions` (`action_id`, `action_name`, `action_detail`) VALUES
(1, 'read', 'Xem'),
(2, 'create', 'Tạo'),
(3, 'edit', 'Sửa'),
(4, 'delete', 'Xoá');

-- --------------------------------------------------------

--
-- Table structure for table `admins_account`
--

CREATE TABLE `admins_account` (
  `admin_id` int(11) NOT NULL,
  `admin_name` varchar(100) NOT NULL,
  `admin_password` varchar(100) NOT NULL,
  `admin_role` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admins_account`
--

INSERT INTO `admins_account` (`admin_id`, `admin_name`, `admin_password`, `admin_role`) VALUES
(1, 'admin', 'pbkdf2:sha256:150000$eNJoRNpd$f3278a88d02190f47dda3f04ab2fd3c1f6929c222ac00f5bf8d03fa6cf79c441', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `bills`
--

CREATE TABLE `bills` (
  `bill_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `fee_ship` int(11) NOT NULL DEFAULT '0',
  `total` int(11) NOT NULL DEFAULT '0',
  `time_create` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bills`
--

INSERT INTO `bills` (`bill_id`, `customer_id`, `fee_ship`, `total`, `time_create`) VALUES
(6, 1, 0, 9200, '2021-04-03 15:17:53'),
(7, 1, 0, 9200, '2021-04-03 15:23:48');

-- --------------------------------------------------------

--
-- Table structure for table `blacklist_token_admin`
--

CREATE TABLE `blacklist_token_admin` (
  `admin_id` int(11) NOT NULL,
  `token` varchar(1000) NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `blacklist_token_customer`
--

CREATE TABLE `blacklist_token_customer` (
  `customer_id` int(11) NOT NULL,
  `token` varchar(1000) NOT NULL,
  `created` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `brands`
--

CREATE TABLE `brands` (
  `brand_id` int(11) NOT NULL,
  `brand_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `brands`
--

INSERT INTO `brands` (`brand_id`, `brand_name`) VALUES
(1, 'Apple'),
(2, 'Samsung'),
(3, 'test');

-- --------------------------------------------------------

--
-- Table structure for table `carts`
--

CREATE TABLE `carts` (
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `carts`
--

INSERT INTO `carts` (`customer_id`, `product_id`, `quantity`) VALUES
(1, 1, 4),
(1, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `comment_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `content` varchar(1000) NOT NULL,
  `time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `customers_account`
--

CREATE TABLE `customers_account` (
  `customer_id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_password` varchar(100) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `customer_address` varchar(100) DEFAULT NULL,
  `customer_phone` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customers_account`
--

INSERT INTO `customers_account` (`customer_id`, `customer_name`, `customer_password`, `customer_email`, `customer_address`, `customer_phone`) VALUES
(1, 'customer', 'pbkdf2:sha256:150000$QheNYrFB$65dbd315da08b1cc81ff4c6f9f16510c83b0cb80234a3f705c9538b6afe89764', '', '1/1 Nguyễn Hữu Thọ', '');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `customer_id` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `last_who_update` int(11) DEFAULT NULL,
  `last_when_update` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `permissions`
--

CREATE TABLE `permissions` (
  `permission_id` int(11) NOT NULL,
  `permission_name` varchar(100) NOT NULL,
  `permission_detail` varchar(254) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `permissions`
--

INSERT INTO `permissions` (`permission_id`, `permission_name`, `permission_detail`) VALUES
(1, 'RoleManager', 'Quản lý quyền'),
(2, 'AccountManager', 'Quản lý tài khoản'),
(3, 'ProductManager', 'Quản lý sản phẩm'),
(4, 'BrandManager', 'Quản lý nhãn hiệu'),
(5, 'CouponManager', 'Quản lý phiếu mua hàng');

-- --------------------------------------------------------

--
-- Table structure for table `permission_role`
--

CREATE TABLE `permission_role` (
  `perm_role_id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL,
  `permission_name` varchar(100) NOT NULL,
  `action_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `permission_role`
--

INSERT INTO `permission_role` (`perm_role_id`, `role_name`, `permission_name`, `action_name`) VALUES
(1, 'admin', 'RoleManager', 'read'),
(2, 'admin', 'RoleManager', 'create'),
(3, 'admin', 'RoleManager', 'edit'),
(5, 'admin', 'RoleManager', 'delete'),
(6, 'admin', 'AccountManager', 'read'),
(7, 'admin', 'AccountManager', 'edit'),
(8, 'admin', 'AccountManager', 'delete'),
(9, 'admin', 'AccountManager', 'create'),
(10, 'admin', 'ProductManager', 'read'),
(11, 'admin', 'ProductManager', 'create'),
(12, 'admin', 'ProductManager', 'edit'),
(13, 'admin', 'ProductManager', 'delete'),
(14, 'admin', 'BrandManager', 'create'),
(15, 'admin', 'BrandManager', 'edit'),
(16, 'admin', 'BrandManager', 'delete'),
(17, 'admin', 'CouponManager', 'read'),
(18, 'admin', 'CouponManager', 'create'),
(19, 'admin', 'CouponManager', 'edit'),
(20, 'admin', 'CouponManager', 'delete');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(200) NOT NULL,
  `brand_id` int(11) DEFAULT NULL,
  `product_thumbnail` varchar(100) DEFAULT NULL,
  `product_description` varchar(1000) DEFAULT NULL,
  `product_default_price` bigint(20) DEFAULT NULL,
  `product_sale_price` bigint(20) DEFAULT NULL,
  `time_warranty` int(11) NOT NULL DEFAULT '0',
  `product_last_update_who` int(11) DEFAULT NULL,
  `product_last_update_when` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `brand_id`, `product_thumbnail`, `product_description`, `product_default_price`, `product_sale_price`, `time_warranty`, `product_last_update_who`, `product_last_update_when`) VALUES
(1, 'IPhone Xsmas', 1, 'no_image.png', 'This is IPhone for description', 1300, 1200, 0, 1, '2021-04-05 15:06:56'),
(2, 'IPhone 12 Pro Max', 1, 'no_image.png', 'This is IPhone Pro Max for description', 2300, 2200, 0, 1, '2021-04-05 15:07:25'),
(3, 'test1', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:11'),
(4, 'test2', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:15'),
(5, 'test3', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:18'),
(6, 'test4', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:22'),
(7, 'test5', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:24'),
(8, 'test6', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:28'),
(9, 'test7', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:31'),
(10, 'test8', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:34'),
(11, 'test9', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:38'),
(12, 'test10', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:41'),
(13, 'test11', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:44'),
(14, 'test12', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:47'),
(15, 'test13', NULL, NULL, NULL, NULL, NULL, 0, 1, '2021-04-02 21:33:51'),
(16, 'test13', NULL, 'no_image.png', NULL, 0, 0, 0, 1, '2021-04-05 14:16:57'),
(17, 'test image', NULL, 'no_image.png', NULL, 0, 0, 0, 1, '2021-04-05 14:24:02'),
(18, 'test image', NULL, 'test_product.png', NULL, 0, 0, 0, 1, '2021-04-05 14:25:04');

-- --------------------------------------------------------

--
-- Table structure for table `product_bill`
--

CREATE TABLE `product_bill` (
  `bill_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product_bill`
--

INSERT INTO `product_bill` (`bill_id`, `product_id`, `quantity`) VALUES
(6, 1, 4),
(6, 2, 2),
(7, 1, 4),
(7, 2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `product_image`
--

CREATE TABLE `product_image` (
  `product_image_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `role_id` int(11) NOT NULL,
  `role_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`role_id`, `role_name`) VALUES
(1, 'admin'),
(3, 'mod'),
(2, 'sales');

-- --------------------------------------------------------

--
-- Table structure for table `warranties`
--

CREATE TABLE `warranties` (
  `warranty` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `start` date NOT NULL,
  `end` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `actions`
--
ALTER TABLE `actions`
  ADD PRIMARY KEY (`action_id`),
  ADD UNIQUE KEY `action_name` (`action_name`);

--
-- Indexes for table `admins_account`
--
ALTER TABLE `admins_account`
  ADD PRIMARY KEY (`admin_id`),
  ADD UNIQUE KEY `admin_name` (`admin_name`) USING BTREE,
  ADD KEY `admin_role` (`admin_role`);

--
-- Indexes for table `bills`
--
ALTER TABLE `bills`
  ADD PRIMARY KEY (`bill_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Indexes for table `blacklist_token_admin`
--
ALTER TABLE `blacklist_token_admin`
  ADD PRIMARY KEY (`admin_id`,`token`);

--
-- Indexes for table `blacklist_token_customer`
--
ALTER TABLE `blacklist_token_customer`
  ADD PRIMARY KEY (`customer_id`,`token`);

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`brand_id`);

--
-- Indexes for table `carts`
--
ALTER TABLE `carts`
  ADD PRIMARY KEY (`customer_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`comment_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `customers_account`
--
ALTER TABLE `customers_account`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `customer_name` (`customer_name`),
  ADD UNIQUE KEY `customer_email` (`customer_email`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`customer_id`,`bill_id`),
  ADD KEY `bill_id` (`bill_id`),
  ADD KEY `last_who_update` (`last_who_update`);

--
-- Indexes for table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`permission_id`),
  ADD UNIQUE KEY `permission_name` (`permission_name`) USING BTREE;

--
-- Indexes for table `permission_role`
--
ALTER TABLE `permission_role`
  ADD PRIMARY KEY (`perm_role_id`),
  ADD KEY `role_name` (`role_name`),
  ADD KEY `function_name` (`permission_name`),
  ADD KEY `function_role_ibfk_3` (`action_name`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`),
  ADD KEY `products_ibfk_1` (`brand_id`),
  ADD KEY `product_last_update_who` (`product_last_update_who`);

--
-- Indexes for table `product_bill`
--
ALTER TABLE `product_bill`
  ADD PRIMARY KEY (`bill_id`,`product_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `product_image`
--
ALTER TABLE `product_image`
  ADD PRIMARY KEY (`product_image_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Indexes for table `warranties`
--
ALTER TABLE `warranties`
  ADD PRIMARY KEY (`warranty`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`),
  ADD KEY `bill_id` (`bill_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `actions`
--
ALTER TABLE `actions`
  MODIFY `action_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `admins_account`
--
ALTER TABLE `admins_account`
  MODIFY `admin_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `bills`
--
ALTER TABLE `bills`
  MODIFY `bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `brand_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `customers_account`
--
ALTER TABLE `customers_account`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `permission_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `permission_role`
--
ALTER TABLE `permission_role`
  MODIFY `perm_role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `product_image`
--
ALTER TABLE `product_image`
  MODIFY `product_image_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `warranties`
--
ALTER TABLE `warranties`
  MODIFY `warranty` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admins_account`
--
ALTER TABLE `admins_account`
  ADD CONSTRAINT `admins_account_ibfk_1` FOREIGN KEY (`admin_role`) REFERENCES `roles` (`role_name`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `bills`
--
ALTER TABLE `bills`
  ADD CONSTRAINT `bills_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `blacklist_token_customer`
--
ALTER TABLE `blacklist_token_customer`
  ADD CONSTRAINT `blacklist_token_customer_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `carts`
--
ALTER TABLE `carts`
  ADD CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`bill_id`) REFERENCES `bills` (`bill_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`last_who_update`) REFERENCES `admins_account` (`admin_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `permission_role`
--
ALTER TABLE `permission_role`
  ADD CONSTRAINT `permission_role_ibfk_1` FOREIGN KEY (`role_name`) REFERENCES `roles` (`role_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `permission_role_ibfk_2` FOREIGN KEY (`permission_name`) REFERENCES `permissions` (`permission_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `permission_role_ibfk_3` FOREIGN KEY (`action_name`) REFERENCES `actions` (`action_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`brand_id`) REFERENCES `brands` (`brand_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `products_ibfk_2` FOREIGN KEY (`product_last_update_who`) REFERENCES `admins_account` (`admin_id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `product_bill`
--
ALTER TABLE `product_bill`
  ADD CONSTRAINT `product_bill_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `bills` (`bill_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `product_bill_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `product_image`
--
ALTER TABLE `product_image`
  ADD CONSTRAINT `product_image_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `warranties`
--
ALTER TABLE `warranties`
  ADD CONSTRAINT `warranties_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `warranties_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `warranties_ibfk_3` FOREIGN KEY (`bill_id`) REFERENCES `bills` (`bill_id`) ON DELETE CASCADE ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS=1;
