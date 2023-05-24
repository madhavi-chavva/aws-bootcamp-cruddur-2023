INSERT INTO public.users (display_name, email, handle, cognito_user_id)
VALUES
  ('Madhavi Chavva', 'mailtomemadhavi2023@gmail.com', 'madhu' ,'MOCK'),
  ('sunrise', 'sunrisemorning264@gmail.com', 'sunrise' ,'MOCK'),
  ('Andrew Bayko', 'bayko@exampro.co', 'bayko' ,'MOCK'),
  ('Londo Mollari','lmollari@centari.com' ,'londo' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'madhu' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )