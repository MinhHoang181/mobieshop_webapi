-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 08, 2021 at 08:06 AM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.1

SET FOREIGN_KEY_CHECKS=0;
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

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
  `fee_ship` int(11) NOT NULL DEFAULT 0,
  `total` int(11) NOT NULL DEFAULT 0,
  `time_create` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

--
-- Dumping data for table `blacklist_token_customer`
--

INSERT INTO `blacklist_token_customer` (`customer_id`, `token`, `created`) VALUES
(1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxNzc4OTcwMiwiZXhwIjoxNjE3NzkzMzAyfQ.eyJjdXN0b21lcl9uYW1lIjoiY3VzdG9tZXIifQ.fUNR0fRrlobbtz1n0hx7hFYH3DOGCwaude98CuoT0av9Qwn0CaGukOhiXbXBof80dbePjxPHo2aYkFp3oWi-2A', '2021-04-07 17:31:48'),
(1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxNzc5Mjg5MCwiZXhwIjoxNjE3Nzk2NDkwfQ.eyJjdXN0b21lcl9uYW1lIjoiY3VzdG9tZXIifQ.nw0T60XiuXpfSgn7caosBVCH9CawKAhVqjc67jh9tpjxqpsSK2YQwBC4OIOLlAssU36U9pG5eASG3tDGhiASPg', '2021-04-07 17:58:45'),
(1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxNzc5ODQ3MCwiZXhwIjoxNjE3ODAyMDcwfQ.eyJjdXN0b21lcl9uYW1lIjoiY3VzdG9tZXIifQ.4yU_q5-54XuIq4b0iRJyLjYirPOlDTUITaLasUMuVr4QvUVwzVWp68qmvXa6-sU4VzWi0BclNtkKmWiRAWLedA', '2021-04-07 19:38:24'),
(1, 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYxNzc5OTEyNCwiZXhwIjoxNjE3ODAyNzI0fQ.eyJjdXN0b21lcl9uYW1lIjoiY3VzdG9tZXIifQ.XhcBBOXeDc51VChsIbh8MMurUl9lDBGO12zybp9DcEOkZ1U6K5tp5VPgx5H1cHU83iSoH0uQaNg-svyhHIiYVA', '2021-04-07 19:39:47');

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
(1, 1, 1);

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
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_password` varchar(100) NOT NULL,
  `customer_email` varchar(100) NOT NULL,
  `customer_address` varchar(100) DEFAULT NULL,
  `customer_phone` varchar(100) DEFAULT NULL,
  `confirmed` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customers_account`
--

INSERT INTO `customers_account` (`customer_id`, `customer_name`, `customer_password`, `customer_email`, `customer_address`, `customer_phone`, `confirmed`) VALUES
(1, 'customer', 'pbkdf2:sha256:150000$QheNYrFB$65dbd315da08b1cc81ff4c6f9f16510c83b0cb80234a3f705c9538b6afe89764', 'xinloima123@gmail.com', '1/1 Nguyễn Hữu Thọ', '0123456789', 1);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `customer_id` int(11) NOT NULL,
  `bill_id` int(11) NOT NULL,
  `address` varchar(1000) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `status` tinyint(1) NOT NULL DEFAULT 0,
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
(5, 'BillManager', 'Quản lý hoá đơn'),
(6, 'OrderManager', 'Quản lý đơn hàng');

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
(17, 'admin', 'BillManager', 'read'),
(18, 'admin', 'BillManager', 'create'),
(19, 'admin', 'BillManager', 'edit'),
(20, 'admin', 'BillManager', 'delete'),
(21, 'admin', 'OrderManager', 'read'),
(22, 'admin', 'OrderManager', 'edit');

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
  `time_warranty` int(11) NOT NULL DEFAULT 0,
  `product_last_update_who` int(11) DEFAULT NULL,
  `product_last_update_when` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `brand_id`, `product_thumbnail`, `product_description`, `product_default_price`, `product_sale_price`, `time_warranty`, `product_last_update_who`, `product_last_update_when`) VALUES
(21, 'iPhone 12 Pro 128GB Chính hãng (VN/A)', 1, 'iphone-12-pro-128gb-vna_3.jpg', 'iPhone 12 Pro 128GB chính hãng (VN/A) bán tại Di Động Việt - Đại lý uỷ quyền chính thức của Apple tại Việt Nam, là phiên bản quốc tế 2 sim (Nano + Esim) chính hãng VN/A. Máy chưa Active + nguyên seal hộp, mới 100% (Fullbox)\n\niPhone 12 Pro 128GB chính hãng (VN/A) là phiên bản được phân phối chính thức bởi Apple Việt Nam, được bảo hành 12 tháng tại Trung tâm Uỷ quyền cao cấp nhất của Apple tại Việt Nam và trên toàn cầu miễn phí. Đồng thời hưởng nhiều ưu đãi, khuyến mãi hấp dẫn tại Di Động Việt.', 30990000, 26790000, 2, 1, '2021-04-08 12:17:40'),
(22, 'iPhone 12 Pro 256GB Chính hãng (VN/A)', 1, 'iphone-12-pro-128gb-vna_3.jpg', 'iPhone 12 Pro 256GB Chính hãng (VN/A) bán tại Di Động Việt - Đại lý uỷ quyền chính thức của Apple tại Việt Nam, là phiên bản quốc tế 2 sim (Nano + Esim) chính hãng VN/A. Máy chưa Active + nguyên seal hộp, mới 100% (Fullbox)\n\niPhone 12 Pro 256GB Chính hãng (VN/A) là phiên bản được phân phối chính thức bởi Apple Việt Nam, được bảo hành 12 tháng tại Trung tâm Uỷ quyền cao cấp nhất của Apple tại Việt Nam và trên toàn cầu miễn phí. Đồng thời hưởng nhiều ưu đãi, khuyến mãi hấp dẫn tại Di Động Việt.', 34990000, 28490000, 2, 1, '2021-04-08 12:19:01'),
(23, 'iPhone 12 Pro Max 128GB Chính hãng (VN/A)', 1, 'iphone-12-pro-max-128gb-vna_1_1.jpg', 'iPhone 12 Pro Max 128GB chính hãng (VN/A) bán tại Di Động Việt - Đại lý uỷ quyền chính thức của Apple tại Việt Nam, là phiên bản quốc tế 2 sim (Nano + Esim) chính hãng VN/A. Máy chưa Active + nguyên seal hộp, mới 100% (Fullbox)\n\niPhone 12 Pro Max 128GB chính hãng (VN/A) là phiên bản được phân phối chính thức bởi Apple Việt Nam, được bảo hành 12 tháng tại Trung tâm Uỷ quyền cao cấp nhất của Apple tại Việt Nam và trên toàn cầu miễn phí. Đồng thời hưởng nhiều ưu đãi, khuyến mãi hấp dẫn tại Di Động Việt.', 33990000, 29390000, 2, 1, '2021-04-08 12:20:41'),
(24, 'iPhone 12 Pro Max 256GB Chính hãng (VN/A)', 1, 'iphone-12-pro-max-128gb-vna_1_1.jpg', 'iPhone 12 Pro Max 256GB chính hãng (VN/A) bán tại Di Động Việt - Đại lý uỷ quyền chính thức của Apple tại Việt Nam, là phiên bản quốc tế 2 sim (Nano + Esim) chính hãng VN/A. Máy chưa Active + nguyên seal hộp, mới 100% (Fullbox)\n\niPhone 12 Pro Max 256GB chính hãng (VN/A) là phiên bản được phân phối chính thức bởi Apple Việt Nam, được bảo hành 12 tháng tại Trung tâm Uỷ quyền cao cấp nhất của Apple tại Việt Nam và trên toàn cầu miễn phí. Đồng thời hưởng nhiều ưu đãi, khuyến mãi hấp dẫn tại Di Động Việt.', 37990000, 31990000, 2, 1, '2021-04-08 12:21:55'),
(25, 'Samsung Galaxy S21 Plus 5G (8GB|256GB)', 2, 'galaxy-s21-plus-black-didongviet_1_1.jpg', 'Samsung Galaxy S21 Plus 5G sở hữu thiết kế hiện đại, đón đầu xu thế mới với màn hình rộng 6.7 inch, cùng công nghệ màn hình Dynamic AMOLED 2X, 120Hz. Máy được trang bị hiệu năng cao cấp, hệ điều hành Android 11, One UI 3.1. Đồng thời camera 64MP cũng là điểm nhấn đặc biệt trên máy.\n\nSamsung Galaxy S21 Plus 5G là điện thoại chính hãng Samsung, nhận bảo hành 12 tháng theo chính sách ủy quyền của Samsung Việt Nam. Đặt mua Galaxy S21 Plus tại Di Động Việt với nhiều ưu đãi đi kèm hấp dẫn.', 28990000, 19390000, 2, 1, '2021-04-08 12:24:04'),
(26, 'Samsung Galaxy S21 Ultra 5G (12GB|256GB)', 2, 'galaxy-s21-ultra-siver-didongviet_1_1.jpg', 'Samsung Galaxy S21 Ultra 5G sở hữu thiết kế sang trọng, đón đầu xu thế mới với màn hình rộng 6.8 inch, cùng công nghệ màn hình Dynamic AMOLED 2X, 120Hz. Máy được trang bị hiệu năng cao cấp, hệ điều hành Android 11, One UI 3.1. Đồng thời camera lên đến 108MP là điểm nổi bật trên phiên bản này.\n\nSamsung Galaxy S21 Ultra 5G là điện thoại chính hãng Samsung, nhận bảo hành 12 tháng theo chính sách ủy quyền của Samsung Việt Nam. Đặt mua Galaxy S21 Ultra 5G tại Di Động Việt với nhiều ưu đãi hấp dẫn.', 33990000, 23590000, 2, 1, '2021-04-08 12:26:39'),
(27, 'Samsung Galaxy A32 (6GB|128GB)', 2, 'samsung-galaxy-a32_1.jpg', 'Samsung Galaxy A32 (6GB|128GB) có thiết kế mới lạ, trẻ trung. Màn hình giọt nước, camera 64 MP, được tích hợp cảm biến vân tay vào nút nguồn.\n\nGalaxy A32 (6GB|128GB) bán tại Di Động Việt là phiên bản chính hãng Samsung Việt Nam, mới 100% với tình trạng nguyên seal máy, nhận bảo hành 12 tháng và hưởng đầy đủ các ưu đãi theo chính sách ủy quyền của Samsung, đồng thời nhận nhiều ưu đãi, khuyến mãi hấp dẫn tại Di Động Việt.', 6690000, 5990000, 2, 1, '2021-04-08 12:28:18');

-- --------------------------------------------------------

--
-- Table structure for table `product_bill`
--

CREATE TABLE `product_bill` (
  `bill_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `product_image`
--

CREATE TABLE `product_image` (
  `product_image_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `image` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `product_image`
--

INSERT INTO `product_image` (`product_image_id`, `product_id`, `image`) VALUES
(4, 21, 'iphone-12-pro-128gb-vna_3.jpg'),
(5, 21, 'iphone-12-pro-max-trang-bac-600x600-200x200.jpg'),
(6, 21, 'iphone-12-pro-max-vang-new-600x600-200x200.jpg'),
(7, 21, 'iphone-12-pro-max-xam-new-600x600-200x200.jpg'),
(8, 22, 'iphone-12-pro-max-trang-bac-600x600-200x200.jpg'),
(9, 22, 'iphone-12-pro-max-vang-new-600x600-200x200.jpg'),
(10, 22, 'iphone-12-pro-max-xam-new-600x600-200x200.jpg'),
(11, 22, 'iphone-12-pro-max-xanh-duong-new-600x600-600x600.jpg'),
(12, 23, 'iphone-12-pro-max-trang-bac-600x600-200x200.jpg'),
(13, 23, 'iphone-12-pro-max-vang-new-600x600-200x200.jpg'),
(14, 23, 'iphone-12-pro-max-xam-new-600x600-200x200.jpg'),
(15, 23, 'iphone-12-pro-max-xanh-duong-new-600x600-600x600.jpg'),
(16, 24, 'iphone-12-pro-max-trang-bac-600x600-200x200.jpg'),
(17, 24, 'iphone-12-pro-max-vang-new-600x600-200x200.jpg'),
(18, 24, 'iphone-12-pro-max-xam-new-600x600-200x200.jpg'),
(19, 24, 'iphone-12-pro-max-xanh-duong-new-600x600-600x600.jpg'),
(20, 25, 's21-plus-5g_1_1_1.jpg'),
(21, 25, 'samsung-galaxy-s21-plus-8gb-256gb.jpg'),
(22, 26, 'samsung-galaxy-s21-ultra-12gb-256gb.jpg'),
(23, 26, 'samsung-galaxy-s21-ultra-12gb-256gb_1.jpg'),
(24, 27, 'samsung-galaxy-a32_1_1.jpg'),
(25, 27, 'samsung-galaxy-a32-den-min.jpg');

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
  ADD UNIQUE KEY `customer_email` (`customer_email`),
  ADD UNIQUE KEY `customer_phone` (`customer_phone`);

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
  MODIFY `bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `brands`
--
ALTER TABLE `brands`
  MODIFY `brand_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `comment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `customers_account`
--
ALTER TABLE `customers_account`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `permissions`
--
ALTER TABLE `permissions`
  MODIFY `permission_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `permission_role`
--
ALTER TABLE `permission_role`
  MODIFY `perm_role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `product_image`
--
ALTER TABLE `product_image`
  MODIFY `product_image_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

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
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
