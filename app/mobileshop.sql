-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 28, 2021 at 12:52 PM
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
  `admin_email` varchar(100) NOT NULL,
  `admin_role` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `admins_account`
--

INSERT INTO `admins_account` (`admin_id`, `admin_name`, `admin_password`, `admin_email`, `admin_role`) VALUES
(1, 'admin', 'pbkdf2:sha256:150000$eNJoRNpd$f3278a88d02190f47dda3f04ab2fd3c1f6929c222ac00f5bf8d03fa6cf79c441', 'test', 'admin');

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
  `cart_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `date_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `carts`
--

INSERT INTO `carts` (`cart_id`, `customer_id`, `product_id`, `quantity`, `date_time`) VALUES
(1, 2, 4, 2, '2021-03-19 10:19:47');

-- --------------------------------------------------------

--
-- Table structure for table `coupon`
--

CREATE TABLE `coupon` (
  `coupon_id` int(11) NOT NULL,
  `coupon_name` varchar(100) NOT NULL,
  `coupon_code` varchar(100) NOT NULL,
  `coupon_discount` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `coupon`
--

INSERT INTO `coupon` (`coupon_id`, `coupon_name`, `coupon_code`, `coupon_discount`) VALUES
(1, 'Apple', 'dsd7116dasd', 17.2),
(2, 'Samsung', 'dasdsadsadsa', 17.2);

-- --------------------------------------------------------

--
-- Table structure for table `customers_account`
--

CREATE TABLE `customers_account` (
  `customer_id` int(11) NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_password` varchar(100) NOT NULL,
  `customer_address` varchar(100) DEFAULT NULL,
  `customer_phone` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customers_account`
--

INSERT INTO `customers_account` (`customer_id`, `customer_name`, `customer_password`, `customer_address`, `customer_phone`) VALUES
(1, 'customer', 'pbkdf2:sha256:150000$bIJTWeV8$7a5ed70a10399da2228144bfcde8d5880497a723068ff74cc37ed4745afdf1e9', 'test', '');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `order_sub_total_price` int(11) DEFAULT NULL,
  `order_shipping` int(11) DEFAULT NULL,
  `coupon_code` varchar(100) DEFAULT NULL,
  `order_total_price` int(11) DEFAULT NULL,
  `order_status` varchar(100) DEFAULT NULL,
  `order_last_update_who` int(11) DEFAULT NULL,
  `order_last_update_when` date DEFAULT NULL
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
  `product_last_update_who` int(11) DEFAULT NULL,
  `product_last_update_when` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `brand_id`, `product_thumbnail`, `product_description`, `product_default_price`, `product_sale_price`, `product_last_update_who`, `product_last_update_when`) VALUES
(1, 'IPhone Xsmas', 1, 'New IPhone 2019', 'This is IPhone for description', 1300, 1200, 1, '2021-03-17 00:00:00'),
(2, 'IPhone 12 Pro Max', 1, 'New IPhone 2020', 'This is IPhone Pro Max for description', 2300, 2200, 1, '2021-03-17 00:00:00');

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
(2, 'sales');

-- --------------------------------------------------------

--
-- Table structure for table `warranty`
--

CREATE TABLE `warranty` (
  `warranty_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `seri_number` int(11) NOT NULL,
  `description` varchar(256) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `date` datetime NOT NULL
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
  ADD UNIQUE KEY `admin_email` (`admin_email`),
  ADD UNIQUE KEY `admin_name` (`admin_name`) USING BTREE,
  ADD KEY `admin_role` (`admin_role`);

--
-- Indexes for table `brands`
--
ALTER TABLE `brands`
  ADD PRIMARY KEY (`brand_id`);

--
-- Indexes for table `carts`
--
ALTER TABLE `carts`
  ADD PRIMARY KEY (`cart_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `coupon`
--
ALTER TABLE `coupon`
  ADD PRIMARY KEY (`coupon_id`);

--
-- Indexes for table `customers_account`
--
ALTER TABLE `customers_account`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `customer_name` (`customer_name`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `order_last_update_who` (`order_last_update_who`);

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
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`role_id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Indexes for table `warranty`
--
ALTER TABLE `warranty`
  ADD PRIMARY KEY (`warranty_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `product_id` (`product_id`);

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
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `brand_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `carts`
--
ALTER TABLE `carts`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `coupon`
--
ALTER TABLE `coupon`
  MODIFY `coupon_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `customers_account`
--
ALTER TABLE `customers_account`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `warranty`
--
ALTER TABLE `warranty`
  MODIFY `warranty_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `admins_account`
--
ALTER TABLE `admins_account`
  ADD CONSTRAINT `admins_account_ibfk_1` FOREIGN KEY (`admin_role`) REFERENCES `roles` (`role_name`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `carts`
--
ALTER TABLE `carts`
  ADD CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`order_last_update_who`) REFERENCES `admins_account` (`admin_id`);

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
-- Constraints for table `warranty`
--
ALTER TABLE `warranty`
  ADD CONSTRAINT `warranty_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers_account` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `warranty_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE ON UPDATE CASCADE;
SET FOREIGN_KEY_CHECKS=1;
