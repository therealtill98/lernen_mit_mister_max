-- init.sql: Erstellt die Tabelle und fügt Beispiel-Daten ein

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT       NOT NULL,
  email TEXT      UNIQUE NOT NULL,
  company TEXT    NOT NULL,
  position TEXT   NOT NULL,
  last_login TIMESTAMP    NOT NULL DEFAULT now(),
  logins_30_days INT       NOT NULL DEFAULT 0,
  seats_company  INT       NOT NULL DEFAULT 0
);

INSERT INTO users (name, email, company, position, last_login, logins_30_days, seats_company) VALUES
  ('Mia Becker',     'mia.becker@firma.de',   'Firma GmbH',   'Entwickler',    now() - INTERVAL '1 days',  12, 50),
  ('Lukas Fischer',  'lukas.fischer@techag.de','Tech AG',      'Manager',       now() - INTERVAL '2 hours',  3,  100),
  ('Emma Wagner',    'emma.wagner@example.com','Example Inc',  'Analyst',       now() - INTERVAL '5 days',   8,  20),
  ('Noah Weber',     'noah.weber@democo.de',   'Demo Co',      'Designer',      now() - INTERVAL '12 hours', 5,  10),
  ('Laura Hoffmann', 'laura.hoffmann@techag.de','Tech AG',      'Entwickler',    now() - INTERVAL '3 days',   15, 100),
  ('Ben Schäfer',    'ben.schaefer@nextcorp.de','Next Corp',    'Engineer',      now() - INTERVAL '7 hours',  7,  75),
  ('Lena Koch',      'lena.koch@firma.de',      'Firma GmbH',   'HR',            now() - INTERVAL '10 days',  2,  50),
  ('Tim Richter',    'tim.richter@example.com','Example Inc',  'Sales',         now() - INTERVAL '4 hours',  9,  20),
  ('Sophie Klein',   'sophie.klein@democo.de',  'Demo Co',      'Analyst',       now() - INTERVAL '6 days',   1,  10),
  ('Paul Wolf',      'paul.wolf@nextcorp.de',   'Next Corp',    'Manager',       now() - INTERVAL '2 days',   11, 75),
  ('Anna Braun',     'anna.braun@firma.de',     'Firma GmbH',   'Developer',     now() - INTERVAL '8 hours',  6,  50),
  ('Jan Neumann',    'jan.neumann@techag.de',   'Tech AG',      'Support',       now() - INTERVAL '15 days',  0,  100),
  ('Sarah Lehmann',  'sarah.lehmann@example.com','Example Inc', 'Designer',      now() - INTERVAL '1 hours',  14, 20),
  ('Felix Hartmann', 'felix.hartmann@democo.de','Demo Co',      'Engineer',      now() - INTERVAL '9 days',   4,  10),
  ('Nina König',     'nina.koenig@nextcorp.de', 'Next Corp',    'Analyst',       now() - INTERVAL '20 hours', 3,  75),
  ('Tim Hoffmann',   'tim.hoffmann@example.com','Example Inc',  'Developer',     now() - INTERVAL '3 hours',  10, 20),
  ('Julia Mayer',    'julia.mayer@techag.de',   'Tech AG',      'HR',            now() - INTERVAL '6 days',   2,  100),
  ('Marco Vogel',    'marco.vogel@firma.de',    'Firma GmbH',   'Sales',         now() - INTERVAL '11 hours', 8,  50),
  ('Lisa Keller',    'lisa.keller@nextcorp.de', 'Next Corp',    'Designer',      now() - INTERVAL '14 days',  1,  75),
  ('David Frank',    'david.frank@democo.de',   'Demo Co',      'Support',       now() - INTERVAL '5 hours',  5,  10);
