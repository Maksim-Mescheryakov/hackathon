
CREATE VIEW CustomerSentiment AS
SELECT 
    CASE
        WHEN conversation LIKE '%негатив%' THEN 'резко негативные'
        WHEN conversation LIKE '%не хочу%' THEN 'резко негативные'
        WHEN conversation LIKE '%не согласен%' THEN 'резко негативные'
        WHEN conversation LIKE '%неинтересно%' THEN 'резко негативные'
        WHEN conversation LIKE '%не понравилось%' THEN 'резко негативные'

        WHEN conversation LIKE '%немного сомневаюсь%' THEN 'слабо негативные'
        WHEN conversation LIKE '%может быть%' THEN 'слабо негативные'
        WHEN conversation LIKE '%не уверен%' THEN 'слабо негативные'
        WHEN conversation LIKE '%неопределенность%' THEN 'слабо негативные'
        WHEN conversation LIKE '%подумаю%' THEN 'слабо негативные'

        WHEN conversation LIKE '%не знаю%' THEN 'нейтральные'
        WHEN conversation LIKE '%не понятно%' THEN 'нейтральные'
        WHEN conversation LIKE '%может быть%' THEN 'нейтральные'
        WHEN conversation LIKE '%пока не готов%' THEN 'нейтральные'
        WHEN conversation LIKE '%не определился%' THEN 'нейтральные'

        WHEN conversation LIKE '%рассмотрю%' THEN 'скорее склонные к покупке'
        WHEN conversation LIKE '%интересное предложение%' THEN 'скорее склонные к покупке'
        WHEN conversation LIKE '%нужно подумать%' THEN 'скорее склонные к покупке'
        WHEN conversation LIKE '%расскажите подробнее%' THEN 'скорее склонные к покупке'
        WHEN conversation LIKE '%интересует услуга%' THEN 'скорее склонные к покупке'

        WHEN conversation LIKE '%готов приобрести%' THEN 'явно заинтересованные'
        WHEN conversation LIKE '%хочу купить%' THEN 'явно заинтересованные'
        WHEN conversation LIKE '%немедленно заключу договор%' THEN 'явно заинтересованные'
        WHEN conversation LIKE '%покупка в ближайшем будущем%' THEN 'явно заинтересованные'
        WHEN conversation LIKE '%заключу сделку%' THEN 'явно заинтересованные'

        ELSE 'неизвестно'
    END AS sentiment_category
FROM CustomerConversations;
