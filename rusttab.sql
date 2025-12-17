CREATE DATABASE IF NOT EXISTS `rusttab`;
USE `rusttab`;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS `users` (
    id_user INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de canciones
CREATE TABLE IF NOT EXISTS `songs` (
    id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL,
    release_date DATE NULL,
    bpm INT DEFAULT 120,
    measures INT DEFAULT 0,
    video_file VARCHAR(255) NOT NULL,
    json_file VARCHAR(255) NOT NULL
);

-- Tabla de favoritos
CREATE TABLE IF NOT EXISTS `favorites` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    song_id VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fav_user FOREIGN KEY (user_id) REFERENCES users(id_user) ON DELETE CASCADE,
    CONSTRAINT fk_fav_song FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    UNIQUE KEY user_song_unique (user_id, song_id)
);

-- Datos de canciones (basado en documentation.txt)
INSERT INTO `songs`(`id`, `title`, `artist`, `release_date`, `bpm`, `measures`, `video_file`, `json_file`) VALUES
('linkinpark_one_step_closer', 'One Step Closer', 'Linkin Park', '2000-09-28', 94, NULL, 'videos/one_step_closer_linkin_park.mp4', 'one_step_closer_linkin_park.json'),
('deftones_my_own_summer', 'My Own Summer (Shove It)', 'Deftones', '1997-12-09', 133, NULL, 'videos/my_own_summer_deftones.mp4', 'my_own_summer_deftones.json'),
('skillet_monster', 'Monster', 'Skillet', '2009-08-25', 138, NULL, 'videos/monster_skillet.mp4', 'monster_skillet.json'),
('threedaysgrace_animal_i_have_become', 'Animal I Have Become', 'Three Days Grace', '2006-04-10', 122, NULL, 'videos/animal_i_have_become_three_days_grace.mp4', 'animal_i_have_become_three_days_grace.json'),
('linkinpark_papercut', 'Papercut', 'Linkin Park', '2000-10-24', 150, NULL, 'videos/papercut_linkin_park.mp4', 'papercut_linkin_park.json'),
('slipknot_duality', 'Duality', 'Slipknot', '2004-05-04', 174, NULL, 'videos/duality_slipknot.mp4', 'duality_slipknot.json'),
('disturbed_down_with_the_sickness', 'Down With The Sickness', 'Disturbed', '2000-03-07', 90, NULL, 'videos/down_with_the_sickness_disturbed.mp4', 'down_with_the_sickness_disturbed.json'),
('korn_freak_on_a_leash', 'Freak on a Leash', 'Korn', '1998-11-09', 105, NULL, 'videos/freak_on_a_leash_korn.mp4', 'freak_on_a_leash_korn.json'),
('slipknot_before_i_forget', 'Before I Forget', 'Slipknot', '2004-05-04', 132, NULL, 'videos/before_i_forget_slipknot.mp4', 'before_i_forget_slipknot.json');
