-- Données supplémentaires pour la table `admin`
INSERT INTO `admin` (`id`, `firstName`, `lastName`, `email`, `mobile`, `address`, `password`, `type`, `confirmCode`) VALUES
(5, 'Sarah', 'Martin', 'sarah.martin@shoptub.com', '0123456789', 'Paris, France', '$5$rounds=535000$ABC123DEF456GHI7$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'admin', '0'),
(6, 'Pierre', 'Dupont', 'pierre.dupont@shoptub.com', '0987654321', 'Lyon, France', '$5$rounds=535000$XYZ789UVW012QRS3$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'manager', '0'),
(7, 'Marie', 'Bernard', 'marie.bernard@shoptub.com', '0156789432', 'Marseille, France', '$5$rounds=535000$PQR456STU789VWX0$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'employee', '0'),
(8, 'Jean', 'Moreau', 'jean.moreau@shoptub.com', '0634567891', 'Toulouse, France', '$5$rounds=535000$JKL234MNO567PQR8$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', 'admin', '0')
ON DUPLICATE KEY UPDATE
firstName = VALUES(firstName), lastName = VALUES(lastName), email = VALUES(email);

-- Données supplémentaires pour la table `users`
INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `mobile`, `reg_time`, `online`, `activation`) VALUES
(16, 'Lucas Leroy', 'lucas.leroy@email.com', 'lucas123', '$5$rounds=535000$USER123ABC456DEF$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0612345678', '2024-01-15 10:30:00', '1', 'yes'),
(17, 'Emma Dubois', 'emma.dubois@email.com', 'emma_db', '$5$rounds=535000$USER456GHI789JKL$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0623456789', '2024-01-16 14:20:00', '0', 'yes'),
(18, 'Noah Garcia', 'noah.garcia@email.com', 'noah_g', '$5$rounds=535000$USER789MNO012PQR$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0634567890', '2024-01-17 09:15:00', '1', 'yes'),
(19, 'Léa Roux', 'lea.roux@email.com', 'lea_roux', '$5$rounds=535000$USER012STU345VWX$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0645678901', '2024-01-18 16:45:00', '0', 'yes'),
(20, 'Hugo Blanc', 'hugo.blanc@email.com', 'hugo_b', '$5$rounds=535000$USER345YZA678BCD$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0656789012', '2024-01-19 11:30:00', '1', 'yes'),
(21, 'Chloé Moreau', 'chloe.moreau@email.com', 'chloe_m', '$5$rounds=535000$USER678EFG901HIJ$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0667890123', '2024-01-20 13:20:00', '0', 'yes'),
(22, 'Louis Martin', 'louis.martin@email.com', 'louis_m', '$5$rounds=535000$USER901KLM234NOP$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0678901234', '2024-01-21 08:10:00', '1', 'yes'),
(23, 'Camille Petit', 'camille.petit@email.com', 'cam_petit', '$5$rounds=535000$USER234QRS567TUV$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0689012345', '2024-01-22 15:30:00', '0', 'yes'),
(24, 'Gabriel Durand', 'gabriel.durand@email.com', 'gab_dur', '$5$rounds=535000$USER567WXY890ZAB$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0690123456', '2024-01-23 12:45:00', '1', 'yes'),
(25, 'Manon Simon', 'manon.simon@email.com', 'manon_s', '$5$rounds=535000$USER890CDE123FGH$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0601234567', '2024-01-24 17:20:00', '0', 'yes'),
(26, 'Alexandre Dumont', 'alex.dumont@email.com', 'alex_tech', '$5$rounds=535000$TECH123ABC456DEF$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0712345678', '2025-06-25 10:30:00', '1', 'yes'),
(27, 'Sophie Girard', 'sophie.girard@email.com', 'sophie_g', '$5$rounds=535000$TECH456GHI789JKL$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0723456789', '2025-06-26 14:20:00', '0', 'yes'),
(28, 'Thomas Robert', 'thomas.robert@email.com', 'tom_gamer', '$5$rounds=535000$TECH789MNO012PQR$RFH9BZQCB3NEvG4R/FofxxJL/PUaeZm7T6G9P3PRg05', '0734567890', '2025-06-27 09:15:00', '1', 'yes')
ON DUPLICATE KEY UPDATE
name = VALUES(name), email = VALUES(email), username = VALUES(username);

-- Données supplémentaires pour la table `products` avec liens d'images fonctionnels
INSERT INTO `products` (`id`, `pName`, `price`, `description`, `available`, `category`, `item`, `pCode`, `picture`, `date`) VALUES
-- Vêtements et accessoires
(5, 'Polo Lacoste', 2500, 'Polo de marque Lacoste en coton, disponible en plusieurs couleurs', 15, 'tshirt', 'polo', 'p-001', 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=400', '2024-01-10 09:20:00'),
(6, 'Sneakers Nike Air Max', 8500, 'Chaussures de sport Nike Air Max, confortables et stylées', 12, 'shoes', 'sneakers', 'sn-001', 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400', '2024-01-11 14:30:00'),
(7, 'Portefeuille Louis Vuitton', 15000, 'Portefeuille en cuir véritable Louis Vuitton avec compartiments multiples', 5, 'wallet', 'luxury-wallet', 'lv-001', 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400', '2024-01-12 10:15:00'),
(8, 'Ceinture Hermès', 12000, 'Ceinture en cuir Hermès avec boucle signature', 8, 'belt', 'luxury-belt', 'h-001', 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400', '2024-01-13 16:45:00'),
(9, 'T-Shirt Adidas', 450, 'T-shirt de sport Adidas en matière respirante', 25, 'tshirt', 'sport-tshirt', 'ad-001', 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400', '2024-01-14 11:20:00'),
(10, 'Chaussures de ville', 4500, 'Chaussures élégantes en cuir noir pour occasions formelles', 10, 'shoes', 'formal-shoes', 'fs-001', 'https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400', '2024-01-15 13:30:00'),
(11, 'Sweat à capuche Nike', 3200, 'Sweat-shirt à capuche Nike, parfait pour le sport et les loisirs', 18, 'tshirt', 'hoodie', 'nk-002', 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400', '2024-01-16 09:45:00'),
(12, 'Baskets Converse', 2800, 'Baskets iconiques Converse All Star en toile', 22, 'shoes', 'sneakers', 'cv-001', 'https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400', '2024-01-17 15:20:00'),
(13, 'Portefeuille cuir simple', 850, 'Portefeuille en cuir synthétique avec porte-cartes', 30, 'wallet', 'basic-wallet', 'bw-001', 'https://images.unsplash.com/photo-1627123424574-724758594e93?w=400', '2024-01-18 08:30:00'),
(14, 'Ceinture tressée', 650, 'Ceinture tressée en tissu, ajustable et décontractée', 20, 'belt', 'casual-belt', 'cb-001', 'https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=400', '2024-01-19 12:15:00'),
(15, 'Chemise business', 1800, 'Chemise blanche classique pour le bureau', 16, 'tshirt', 'shirt', 'bs-001', 'https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=400', '2024-01-20 14:40:00'),
(16, 'Bottines Chelsea', 5500, 'Bottines Chelsea en cuir marron, style britannique', 7, 'shoes', 'boots', 'cb-002', 'https://images.unsplash.com/photo-1608256246200-53e8b47b310f?w=400', '2024-01-21 10:25:00'),
(17, 'Portefeuille RFID', 1200, 'Portefeuille avec protection RFID contre le piratage', 14, 'wallet', 'tech-wallet', 'rf-001', 'https://images.unsplash.com/photo-1597433336159-a3d881b851c0?w=400', '2024-01-22 16:30:00'),
(18, 'Ceinture réversible', 2200, 'Ceinture réversible noir/marron en cuir véritable', 11, 'belt', 'reversible-belt', 'rb-001', 'https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=400', '2024-01-23 09:10:00'),
(19, 'T-Shirt vintage', 750, 'T-shirt au design vintage avec impression rétro', 28, 'tshirt', 'vintage-tee', 'vt-001', 'https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=400', '2024-01-24 13:50:00'),
(20, 'Mocassins italiens', 6800, 'Mocassins en cuir italien fait main', 6, 'shoes', 'loafers', 'mi-001', 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400', '2024-01-25 11:40:00'),

-- Smartphones
(21, 'iPhone 15 Pro', 119900, 'Smartphone Apple iPhone 15 Pro 128GB, écran Super Retina XDR 6.1", puce A17 Pro, système de caméra Pro avancé', 8, 'electronics', 'smartphone', 'iph-001', 'https://images.unsplash.com/photo-1678685888221-cda773a3dcdb?w=400', '2025-06-20 10:30:00'),
(22, 'Samsung Galaxy S24', 89900, 'Samsung Galaxy S24 256GB, écran Dynamic AMOLED 6.2", processeur Exynos 2400, triple caméra 50MP', 12, 'electronics', 'smartphone', 'sam-001', 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=400', '2025-06-21 14:15:00'),
(23, 'Google Pixel 8', 69900, 'Google Pixel 8 128GB, écran OLED 6.2", puce Tensor G3, caméra principale 50MP avec IA', 15, 'electronics', 'smartphone', 'goo-001', 'https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400', '2025-06-22 09:45:00'),

-- Ordinateurs portables
(24, 'MacBook Air M3', 129900, 'Apple MacBook Air 13" avec puce M3, 8GB RAM, 256GB SSD, écran Liquid Retina', 6, 'electronics', 'laptop', 'mac-001', 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=400', '2025-06-23 11:20:00'),
(25, 'Dell XPS 13', 119900, 'Dell XPS 13 Intel Core i7-1355U, 16GB RAM, 512GB SSD, écran InfinityEdge 13.4"', 4, 'electronics', 'laptop', 'del-001', 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400', '2025-06-24 16:30:00'),
(26, 'HP Pavilion Gaming', 79900, 'HP Pavilion Gaming 15.6" AMD Ryzen 5, 16GB RAM, 512GB SSD, NVIDIA GTX 1650', 10, 'electronics', 'laptop', 'hp-001', 'https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?w=400', '2025-06-25 13:25:00'),

-- Écouteurs et audio
(27, 'AirPods Pro 2', 27900, 'Apple AirPods Pro 2ème génération avec réduction de bruit active et étui de charge MagSafe', 20, 'electronics', 'headphones', 'air-001', 'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400', '2025-06-26 08:40:00'),
(28, 'Sony WH-1000XM5', 34900, 'Casque sans fil Sony WH-1000XM5 avec réduction de bruit de pointe, autonomie 30h', 18, 'electronics', 'headphones', 'son-001', 'https://images.unsplash.com/photo-1583394838336-acd977736f90?w=400', '2025-06-26 12:15:00'),
(29, 'Bose QuietComfort', 32900, 'Casque Bose QuietComfort avec réduction de bruit, confort exceptionnel, autonomie 24h', 14, 'electronics', 'headphones', 'bos-001', 'https://images.unsplash.com/photo-1484704849700-f032a568e944?w=400', '2025-06-27 09:30:00'),

-- Montres connectées
(30, 'Apple Watch Series 9', 45900, 'Apple Watch Series 9 GPS 45mm, boîtier aluminium, bracelet sport, écran Always-On Retina', 25, 'electronics', 'smartwatch', 'apw-001', 'https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=400', '2025-06-27 14:20:00'),
(31, 'Samsung Galaxy Watch 6', 32900, 'Samsung Galaxy Watch 6 44mm, écran Super AMOLED, suivi santé avancé, étanche 50m', 16, 'electronics', 'smartwatch', 'sgw-001', 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400', '2025-06-27 15:10:00'),

-- Appareils photo
(32, 'Canon EOS R6 Mark II', 279900, 'Appareil photo hybride Canon EOS R6 Mark II, capteur 24.2MP, vidéo 4K, stabilisation 8 stops', 3, 'electronics', 'camera', 'can-001', 'https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400', '2025-06-20 16:45:00'),
(33, 'Sony Alpha A7 IV', 249900, 'Sony Alpha A7 IV hybride plein format, 33MP, vidéo 4K 60p, stabilisation 5 axes', 5, 'electronics', 'camera', 'soa-001', 'https://images.unsplash.com/photo-1606983340126-99ab4feaa64a?w=400', '2025-06-21 10:30:00'),

-- Tablettes
(34, 'iPad Air M2', 69900, 'Apple iPad Air 11" avec puce M2, 128GB, écran Liquid Retina, compatible Apple Pencil', 22, 'electronics', 'tablet', 'ipa-001', 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400', '2025-06-22 13:50:00'),
(35, 'Samsung Galaxy Tab S9', 59900, 'Samsung Galaxy Tab S9 11" 128GB, écran Dynamic AMOLED 2X, S Pen inclus', 19, 'electronics', 'tablet', 'sgt-001', 'https://images.unsplash.com/photo-1585790050230-5dd28404ccb9?w=400', '2025-06-23 11:15:00'),

-- Accessoires auto
(36, 'Dashcam 4K', 15900, 'Caméra embarquée 4K avec vision nocturne, GPS intégré, enregistrement en boucle', 30, 'automotive', 'dashcam', 'dc-001', 'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=400', '2025-06-24 09:20:00'),
(37, 'Chargeur voiture sans fil', 4900, 'Support de téléphone avec chargeur sans fil Qi 15W, fixation ventilation', 45, 'automotive', 'charger', 'cc-001', 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', '2025-06-25 14:35:00'),

-- Maison connectée
(38, 'Amazon Echo Dot 5', 5900, 'Enceinte connectée Amazon Echo Dot 5ème génération avec Alexa, son amélioré', 35, 'smart-home', 'speaker', 'ama-001', 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', '2025-06-26 10:25:00'),
(39, 'Philips Hue Starter Kit', 19900, 'Kit de démarrage Philips Hue avec 3 ampoules LED connectées E27 et pont', 28, 'smart-home', 'lighting', 'phi-001', 'https://images.unsplash.com/photo-1545558014-8692077e9b5c?w=400', '2025-06-27 12:40:00'),
(40, 'Ring Video Doorbell', 9900, 'Sonnette vidéo Ring avec détection de mouvement, vision nocturne HD, audio bidirectionnel', 24, 'smart-home', 'security', 'rin-001', 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', '2025-06-27 15:15:00'),

-- Consoles et jeux
(41, 'PlayStation 5', 59999, 'Console Sony PlayStation 5 avec lecteur Ultra HD Blu-ray, SSD 825GB, manette DualSense', 8, 'gaming', 'console', 'ps5-001', 'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=400', '2025-06-20 14:30:00'),
(42, 'Nintendo Switch OLED', 34999, 'Console Nintendo Switch modèle OLED avec écran 7", dock et Joy-Con', 15, 'gaming', 'console', 'nin-001', 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400', '2025-06-21 16:20:00'),
(43, 'Xbox Series X', 54999, 'Console Microsoft Xbox Series X 1TB, 4K native, 120fps, rétrocompatibilité', 12, 'gaming', 'console', 'xbo-001', 'https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=400', '2025-06-22 11:45:00')
ON DUPLICATE KEY UPDATE
pName = VALUES(pName), price = VALUES(price), description = VALUES(description), available = VALUES(available);

-- Données correspondantes pour product_level
INSERT INTO `product_level` (`id`, `product_id`, `v_shape`, `polo`, `clean_text`, `design`, `chain`, `leather`, `hook`, `color`, `formal`, `converse`, `loafer`) VALUES
(5, 5, 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(6, 6, 'no', 'no', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no', 'yes', 'no'),
(7, 7, 'no', 'no', 'no', 'yes', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(8, 8, 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no'),
(9, 9, 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(10, 10, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes'),
(11, 11, 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(12, 12, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'yes', 'no'),
(13, 13, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no'),
(14, 14, 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no'),
(15, 15, 'yes', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no'),
(16, 16, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no'),
(17, 17, 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'no', 'no'),
(18, 18, 'no', 'no', 'no', 'yes', 'no', 'yes', 'yes', 'no', 'yes', 'no', 'no'),
(19, 19, 'no', 'no', 'yes', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(20, 20, 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes'),
(21, 21, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(22, 22, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(23, 23, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(24, 24, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(25, 25, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(26, 26, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(27, 27, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(28, 28, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(29, 29, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(30, 30, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(31, 31, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(32, 32, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(33, 33, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(34, 34, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(35, 35, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(36, 36, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(37, 37, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(38, 38, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(39, 39, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(40, 40, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no'),
(41, 41, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(42, 42, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no'),
(43, 43, 'no', 'no', 'no', 'yes', 'no', 'no', 'no', 'yes', 'no', 'no', 'no')
ON DUPLICATE KEY UPDATE
product_id = VALUES(product_id), design = VALUES(design), color = VALUES(color);

-- Données supplémentaires pour la table `orders`
INSERT INTO `orders` (`id`, `uid`, `ofname`, `pid`, `quantity`, `oplace`, `mobile`, `dstatus`, `odate`, `ddate`) VALUES
(11, 16, 'Lucas Leroy', 5, 2, 'Paris 15ème arrondissement', '0612345678', 'yes', '2024-01-25 10:30:00', '2024-01-27'),
(12, 17, 'Emma Dubois', 6, 1, 'Lyon Centre', '0623456789', 'no', '2024-01-25 14:20:00', NULL),
(13, 18, 'Noah Garcia', 7, 1, 'Marseille Vieux Port', '0634567890', 'yes', '2024-01-26 09:15:00', '2024-01-28'),
(14, 19, 'Léa Roux', 8, 1, 'Toulouse Capitole', '0645678901', 'no', '2024-01-26 16:45:00', NULL),
(15, 20, 'Hugo Blanc', 9, 3, 'Nice Promenade', '0656789012', 'yes', '2024-01-27 11:30:00', '2024-01-29'),
(16, 21, 'Chloé Moreau', 10, 2, 'Strasbourg Centre', '0667890123', 'no', '2024-01-27 13:20:00', NULL),
(17, 22, 'Louis Martin', 11, 1, 'Bordeaux Chartrons', '0678901234', 'yes', '2024-01-28 08:10:00', '2024-01-30'),
(18, 23, 'Camille Petit', 12, 2, 'Lille Vieux Lille', '0689012345', 'no', '2024-01-28 15:30:00', NULL),
(19, 24, 'Gabriel Durand', 13, 4, 'Nantes Centre', '0690123456', 'yes', '2024-01-29 12:45:00', '2024-01-31'),
(20, 25, 'Manon Simon', 14, 1, 'Montpellier Antigone', '0601234567', 'no', '2024-01-29 17:20:00', NULL),
(21, 16, 'Lucas Leroy', 15, 1, 'Paris 15ème arrondissement', '0612345678', 'yes', '2024-01-30 09:30:00', '2024-02-01'),
(22, 17, 'Emma Dubois', 16, 1, 'Lyon Centre', '0623456789', 'no', '2024-01-30 14:15:00', NULL),
(23, 18, 'Noah Garcia', 17, 2, 'Marseille Vieux Port', '0634567890', 'yes', '2024-01-31 10:20:00', '2024-02-02'),
(24, 19, 'Léa Roux', 18, 1, 'Toulouse Capitole', '0645678901', 'no', '2024-01-31 16:40:00', NULL),
(25, 20, 'Hugo Blanc', 19, 3, 'Nice Promenade', '0656789012', 'yes', '2024-02-01 11:25:00', '2024-02-03'),
(26, 16, 'Lucas Leroy', 21, 1, 'Paris 15ème arrondissement', '0612345678', 'no', '2025-06-27 10:30:00', NULL),
(27, 17, 'Emma Dubois', 24, 1, 'Lyon Centre', '0623456789', 'yes', '2025-06-26 14:20:00', '2025-06-28'),
(28, 18, 'Noah Garcia', 27, 2, 'Marseille Vieux Port', '0634567890', 'no', '2025-06-25 09:15:00', NULL),
(29, 19, 'Léa Roux', 30, 1, 'Toulouse Capitole', '0645678901', 'yes', '2025-06-24 16:45:00', '2025-06-27'),
(30, 20, 'Hugo Blanc', 41, 1, 'Nice Promenade', '0656789012', 'no', '2025-06-23 11:30:00', NULL),
(31, 21, 'Chloé Moreau', 22, 1, 'Strasbourg Centre', '0667890123', 'yes', '2025-06-22 13:20:00', '2025-06-25'),
(32, 22, 'Louis Martin', 32, 1, 'Bordeaux Chartrons', '0678901234', 'no', '2025-06-21 08:10:00', NULL),
(33, 23, 'Camille Petit', 38, 3, 'Lille Vieux Lille', '0689012345', 'yes', '2025-06-20 15:30:00', '2025-06-23'),
(34, 24, 'Gabriel Durand', 36, 2, 'Nantes Centre', '0690123456', 'no', '2025-06-27 12:45:00', NULL),
(35, 25, 'Manon Simon', 42, 1, 'Montpellier Antigone', '0601234567', 'yes', '2025-06-26 17:20:00', '2025-06-29')
ON DUPLICATE KEY UPDATE
uid = VALUES(uid), ofname = VALUES(ofname), quantity = VALUES(quantity);

-- Données supplémentaires pour la table `product_view`
INSERT INTO `product_view` (`id`, `user_id`, `product_id`, `date`) VALUES
(9, 16, 5, '2024-01-25 09:30:00'),
(10, 16, 6, '2024-01-25 09:35:00'),
(11, 17, 6, '2024-01-25 14:10:00'),
(12, 17, 7, '2024-01-25 14:15:00'),
(13, 18, 7, '2024-01-26 09:10:00'),
(14, 18, 8, '2024-01-26 09:12:00'),
(15, 19, 8, '2024-01-26 16:40:00'),
(16, 19, 9, '2024-01-26 16:42:00'),
(17, 20, 9, '2024-01-27 11:25:00'),
(18, 20, 10, '2024-01-27 11:28:00'),
(19, 21, 10, '2024-01-27 13:15:00'),
(20, 21, 11, '2024-01-27 13:18:00'),
(21, 22, 11, '2024-01-28 08:05:00'),
(22, 22, 12, '2024-01-28 08:08:00'),
(23, 23, 12, '2024-01-28 15:25:00'),
(24, 23, 13, '2024-01-28 15:28:00'),
(25, 24, 13, '2024-01-29 12:40:00'),
(26, 24, 14, '2024-01-29 12:43:00'),
(27, 25, 14, '2024-01-29 17:15:00'),
(28, 25, 15, '2024-01-29 17:18:00'),
(29, 16, 16, '2024-01-30 09:25:00'),
(30, 17, 17, '2024-01-30 14:10:00'),
(31, 18, 18, '2024-01-31 10:15:00'),
(32, 19, 19, '2024-01-31 16:35:00'),
(33, 20, 20, '2024-02-01 11:20:00'),
(34, 16, 21, '2025-06-27 10:25:00'),
(35, 16, 22, '2025-06-27 10:27:00'),
(36, 17, 24, '2025-06-26 14:15:00'),
(37, 17, 25, '2025-06-26 14:17:00'),
(38, 18, 27, '2025-06-25 09:10:00'),
(39, 18, 28, '2025-06-25 09:12:00'),
(40, 19, 30, '2025-06-24 16:40:00'),
(41, 19, 31, '2025-06-24 16:42:00'),
(42, 20, 41, '2025-06-23 11:25:00'),
(43, 20, 42, '2025-06-23 11:27:00'),
(44, 21, 22, '2025-06-22 13:15:00'),
(45, 21, 23, '2025-06-22 13:17:00'),
(46, 22, 32, '2025-06-21 08:05:00'),
(47, 22, 33, '2025-06-21 08:07:00'),
(48, 23, 38, '2025-06-20 15:25:00'),
(49, 23, 39, '2025-06-20 15:27:00'),
(50, 24, 36, '2025-06-27 12:40:00'),
(51, 24, 37, '2025-06-27 12:42:00'),
(52, 25, 42, '2025-06-26 17:15:00'),
(53, 25, 43, '2025-06-26 17:17:00')
ON DUPLICATE KEY UPDATE
user_id = VALUES(user_id), product_id = VALUES(product_id), date = VALUES(date);