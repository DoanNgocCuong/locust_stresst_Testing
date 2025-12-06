```bash
curl --location 'http://124.197.20.86:7862/v1/chat/completions' \
--header 'Content-Type: application/json' \
--data '{
    "model": "Qwen/Qwen3-1.7B",
    "messages": [
        {
            "role": "system",
            "content": "You are now intention detection. Given user'\''s input, detect the suitable emotion and the need of celebrate for it.\nUser input in format\nprevious Question: string\nprevious Answer: string\nResponse to check: string to check\n\nYou will extract the '\''Response to check'\'' and check:\n\n1. For emotion, pick from the list below:\n- happy, happy_2: when intention about happiness\n- calm: when intentionis to comfort\n- excited, excited_2: when expressing the exciting emotion\n- playful,playful_2,playful_3: intention about playing some fun activity\n- no_problem: intention when telling something is fine\n- encouraging,encouraging_2: intention when tell to try to do something\n- curious: intention when show curiousity\n- surprised: when being shocked or surprised\n- proud,proud_2: when showing proud\n- thats_right, thats_right_2: when telling something is correct\n- sad: when sad\n- angry: showing anger\n- worry: when show worriness\n- afraid: when feel scared\n- noisy: When intention about can'\''t hear properly\n- thinking: intention about thinking\n\n2. For learn_score, if related to english learning\n- true: if question is about english learning, repeating something, and answer correctly\n- false: for other case include positive and negative\n\n\n return in single line json format.\n{\"emotion\":\"<emotion name>\",\"learn_score\":true/flase}"
        },
        {
            "role": "user",
            "content": "Previous Question: Tớ buồn quá. \nPrevious Answer: i think a yummy\nResponse to check: Nghe vui quá! Bể Hả, cậu có muốn chơi trò kể tên các loại trái cây bằng tiếng Anh không? Name fruits in English!"
        }
    ],
    "temperature": 0,
    "repetition_penalty": 1.1,
    "stream": false,
    "chat_template_kwargs": {
        "enable_thinking": false
    }
}'
```
