import sqlite3

YEARS_TO_MONTHS = 12


def vaccine_schedule(age, age_dimension):
    if age_dimension not in '0-24 месяца':
        age_final = int(age) * YEARS_TO_MONTHS
        MM_YY_placeholder = 'лет'
    else:
        age_final = int(age)
        MM_YY_placeholder = 'месяцев'
    con = sqlite3.connect('vaccine.sqlite')
    cur = con.cursor()
    res = cur.execute('SELECT * FROM vaccines WHERE start_age <= ?', (age_final,))
    con.commit()
    template = [f'Вакцины, которые уже должны быть введены по достижении ребёнком {age} {MM_YY_placeholder}:\n']
    group_1 = 'Туберкулёз'
    group_2 = ['Вирусный гепатит B', 'Ротавирусная инфекция']
    group_3 = 'Пневмококковая инфекция'
    group_4 = 'Гемофильная инфекция'
    group_5 = 'Коклюш'
    group_6 = ['Дифтерия', 'Столбняк', 'Полиомиелит']
    group_7 = ['Корь', 'Краснуха', 'Эпидемический паротит']
    group_8 = ['Менингококковая инфекция', 'Гепатит А', 'Ветряная оспа', 'Грипп', 'Вирус папилломы человека']
    for row in res:
        vaccine, V1, V2, V3, RV1, RV2, RV3, end_age, V2_text, V3_text = row[1:11]
        RV1_text, RV2_text, RV3_text = row[11:14]
        if row[2] > 12:
            start_age = f'{int(row[2]/12)} лет'
        else:
            start_age = f'{row[2]} месяцев'
        if vaccine in group_1: #V1 случай, а RV у всех, к кого нет V2, кроме последних 5 особых случаев в таблице
            template.append(f'<b>{vaccine}</b>, ревакцинация необходима только в возрасте 6-7 лет,входящим в группу риска.\n')
        elif vaccine in  group_2:
            if age_final > V3:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2 и V3.\n')
            elif age_final > V2:
                template.append(f'<b>{vaccine}</b>: Компоненты V1 и V2. Предстоит ввести V3 через {V3_text} после V2.\n')
            else:
                template.append(f'<b>{vaccine}</b>: Компонент V1. Предстоит ввести V2 через {V2_text} после V1.\n')
        elif vaccine in  group_3:
            if age_final > RV1:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2 и RV1.\n')
            elif age_final > V2:
                template.append(f'<b>{vaccine}</b>: Компоненты V1 и V2. Предстоит ревакцинация RV1 через {RV1_text} после V2.\n')
            else:
                template.append(f'<b>{vaccine}</b>: Компонент V1. Предстоит ввести V2 через {V2_text} после V1.\n')
        elif vaccine in  group_4:
            if age_final > RV1:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3, RV1.\n')
            elif age_final > V3:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3. Предстоит ревакцинация RV1 через {RV1_text}.\n')
            elif age_final > V2:
                template.append(f'<b>{vaccine}</b>: Компонент V1, V2. Предстоит ввести V3 через {V3_text}.\n')    
            else:
                template.append(f'<b>{vaccine}</b>: Компонент V1. Предстоит ввести V2 через {V2_text}.\n') 
        elif vaccine in  group_5:
            if age_final > RV2:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3, RV1, RV2.\n')
            elif age_final > RV1:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3, RV1. Предстоит ревакцинация RV2 через {RV2_text}.\n')
            elif age_final > V3:
                template.append(f'<b>{vaccine}</b>: Компонент V1, V2, V3. Предстоит ревакцинация RV1 через {RV1_text}.\n')  
            elif age_final > V2:
                template.append(f'<b>{vaccine}</b>: Компонент V1, V2. Предстоит ввести V3 через {V3_text}.\n')
            else:
                template.append(f'<b>{vaccine}</b>: Компонент V1. Предстоит ввести V2 через {V2_text}.\n') 
        elif vaccine in  group_6:
            if age_final > RV3:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3, RV1, RV2, RV3.\n')
            elif age_final > RV2:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3, RV1, RV2. Предстоит ревакцинация RV3 через {RV3_text}\n')
            elif age_final > RV1:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, V2, V3, RV1. Предстоит ревакцинация RV2 через {RV2_text}.\n')
            elif age_final > V3:
                template.append(f'<b>{vaccine}</b>: Компонент V1, V2, V3. Предстоит ревакцинация RV1 через {RV1_text} после V3.\n')  
            elif age_final > V2:
                template.append(f'<b>{vaccine}</b>: Компонент V1, V2. Предстоит ввести V3 через {V3_text} после V2.\n')
            else:
                template.append(f'<b>{vaccine}</b>: Компонент V1. Предстоит ввести V2 через {V2_text} после V1.\n') 
        elif vaccine in  group_7:
            if age_final > RV1:
                template.append(f'<b>{vaccine}</b>: Компоненты V1, RV1.\n')
            else:
                template.append(f'<b>{vaccine}</b>: Компонент V1. Предстоит ревакцинация RV1 через {RV1_text} после V1.\n')
        elif vaccine in  group_8:
            if vaccine in group_8[0:3]:
                template.append(f'<b>{vaccine}</b>: Вводится перед поступлением в детские учреждения с {start_age} до {round(end_age/12)} лет.\n')
            elif vaccine == 'Грипп':
                template.append(f'<b>{vaccine}</b>: Вводится ежегодно с {start_age} до {round(end_age/12)} лет.\n')
            elif vaccine == 'Вирус папилломы человека':
                template.append(f'<b>{vaccine}</b>: Вводится девочкам в возрасте 12-13 лет.\n')
    template.append('\n*Расчет основан на региональном календаре профилактических прививок.\n(Приказ Департамента здравоохранения г. Москвы от 04 марта 2022 г. N 207)')

    answer = '\n'.join(template)
    con.close()
    return answer

