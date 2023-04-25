-- add superuser; login: "gendo.ikari@nerv.jp", password: "gendowned"
INSERT INTO user VALUES (1, 'Gendo Ikari', 'gendo.ikari@nerv.jp', '$2b$12$kFOcNVpEOK3joUWXWX45i.dnsIbKInwE/6JwOH.YEot91ySX1fLju', true); -- `gendowned`
-- add trader Shinji; login: "shinji.ikari@nerv.jp", password: "gendowned", trader_id: "eva_01"
INSERT INTO user VALUES (2, 'Shinji Ikari', 'shinji.ikari@nerv.jp', '$2b$12$kFOcNVpEOK3joUWXWX45i.dnsIbKInwE/6JwOH.YEot91ySX1fLju', false); -- `gendowned`
INSERT INTO trader VALUES ('eva_01', 2);
-- add trader Asuka; login: "asuka.langley.soryu@nerv.de", password: "gendowned", trader_id: "eva_02"
INSERT INTO user VALUES (3, 'Asuka Langley Soryu', 'asuka.langley.soryu@nerv.de', '$2b$12$kFOcNVpEOK3joUWXWX45i.dnsIbKInwE/6JwOH.YEot91ySX1fLju', false); -- `gendowned`
INSERT INTO trader VALUES ('eva_02', 3);

-- buy price: 15, sell price: 20
-- trader Shinji bought less, sold more
INSERT INTO trade VALUES ('trade_01_1', 'eva_01', 15, 10, 'buy', CURRENT_DATE, 9, CURRENT_TIMESTAMP);
INSERT INTO trade VALUES ('trade_01_2', 'eva_01', 16, 10, 'buy', CURRENT_DATE, 9, CURRENT_TIMESTAMP);
INSERT INTO trade VALUES ('trade_01_3', 'eva_01', 20, 20, 'sell', CURRENT_DATE, 9, CURRENT_TIMESTAMP);
-- trader Shinji sold less, bought more
INSERT INTO trade VALUES ('trade_01_4', 'eva_01', 15, 50, 'buy', CURRENT_DATE, 10, CURRENT_TIMESTAMP);
INSERT INTO trade VALUES ('trade_01_5', 'eva_01', 20, 30, 'sell', CURRENT_DATE, 10, CURRENT_TIMESTAMP);

-- buy price: 20, sell price: 30
-- trader Asuka bought less, sold more
INSERT INTO trade VALUES ('trade_02_1', 'eva_02', 200, 10, 'buy', CURRENT_DATE, 9, CURRENT_TIMESTAMP);
INSERT INTO trade VALUES ('trade_02_2', 'eva_02', 30, 25, 'sell', CURRENT_DATE, 9, CURRENT_TIMESTAMP);
-- trader Asuka sold less, bought more
INSERT INTO trade VALUES ('trade_02_4', 'eva_02', 20, 50, 'buy', CURRENT_DATE, 10, CURRENT_TIMESTAMP);
INSERT INTO trade VALUES ('trade_02_5', 'eva_02', 30, 35, 'sell', CURRENT_DATE, 10, CURRENT_TIMESTAMP);
-- other hours
INSERT INTO trade VALUES ('trade_02_6', 'eva_02', 20, 54, 'buy', CURRENT_DATE, 18, CURRENT_TIMESTAMP);
INSERT INTO trade VALUES ('trade_02_3', 'eva_02', 30, 79, 'sell', CURRENT_DATE, 18, CURRENT_TIMESTAMP);
-- only one operation in hour
INSERT INTO trade VALUES ('trade_02_7', 'eva_02', 35, 5, 'buy', CURRENT_DATE, 23, CURRENT_TIMESTAMP);
