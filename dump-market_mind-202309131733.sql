-- market_mind.alpha_vantage_agg definition

CREATE TABLE `alpha_vantage_agg` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_recorded` timestamp NULL DEFAULT NULL,
  `avg_score` float DEFAULT NULL,
  `max_score` float DEFAULT NULL,
  `min_score` float DEFAULT NULL,
  `std_score` float DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uc_alpha_vantage_date` (`date_recorded`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.alpha_vantage_news_with_sentiment definition

CREATE TABLE `alpha_vantage_news_with_sentiment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` text,
  `url` text,
  `time_published` timestamp NULL DEFAULT NULL,
  `summary` text,
  `banner_image` text,
  `source` varchar(255) DEFAULT NULL,
  `category_within_source` varchar(255) DEFAULT NULL,
  `source_domain` varchar(255) DEFAULT NULL,
  `overall_sentiment_score` float DEFAULT NULL,
  `overall_sentiment_label` varchar(25) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10865 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.emotion definition

CREATE TABLE `emotion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(55) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uc_emotion_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.reddit_agg definition

CREATE TABLE `reddit_agg` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_recorded` timestamp NULL DEFAULT NULL,
  `emotion_name` varchar(55) DEFAULT NULL,
  `avg_score` float DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uc_reddit_date_emotion` (`date_recorded`,`emotion_name`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.reddit_comment_clean definition

CREATE TABLE `reddit_comment_clean` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.reddit_comment_emotion definition

CREATE TABLE `reddit_comment_emotion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment_id` bigint DEFAULT NULL,
  `emotion_id` bigint DEFAULT NULL,
  `score` float DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93813 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.reddit_comment_raw definition

CREATE TABLE `reddit_comment_raw` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comment` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15262 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


-- market_mind.trades definition

CREATE TABLE `trades` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `symbol` varchar(255) DEFAULT NULL,
  `trade_conditions` varchar(255) DEFAULT NULL,
  `price` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `trade_timestamp` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `trade_timestamp_index` (`trade_timestamp`)
) ENGINE=InnoDB AUTO_INCREMENT=1291875 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;