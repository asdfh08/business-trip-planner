-- ==========================================================
-- Сервис планирования командировок: SQL-запросы проекта
-- ==========================================================
-- Конкретные значения (id, даты, пороги) указаны для проверки
-- в консоли SQLite. В Django-представлениях вместо них стоит
-- заполнитель ?, а значение передаётся отдельным параметром.
--
-- Где используется запрос:
--   1      /                       главная (сводка)
--   2      /employees/             список сотрудников
--   3-5    /employees/<id>/        карточка сотрудника
--   6      /employees/available/   свободные сотрудники на дату
--   7-8    /trips/                 список командировок (+ фильтр)
--   9      /trips/<id>/            карточка командировки
--   10-14  /trips/statistics/      статистика


-- 1. Сводка для главной страницы: число сотрудников
--    и активных командировок (агрегатная функция COUNT)
SELECT
    (SELECT COUNT(*) FROM employees) AS employees_count,
    (SELECT COUNT(*) FROM trips WHERE is_cancelled = 0)
        AS active_trips_count;


-- 2. Список сотрудников, отсортированный по ФИО (выборка списка)
SELECT
    id,
    name,
    position
FROM employees
ORDER BY name;


-- 3. Сотрудник по идентификатору (фильтрация WHERE)
--    В приложении: WHERE id = ?
SELECT
    id,
    name,
    position
FROM employees
WHERE id = 1;


-- 4. Командировки сотрудника с маршрутом (JOIN + WHERE)
--    В приложении: WHERE trips.employee_id = ?
SELECT
    trips.id,
    trips.start_date,
    trips.end_date,
    trips.is_cancelled,
    routes.origin,
    routes.destination
FROM trips
JOIN routes ON trips.route_id = routes.id
WHERE trips.employee_id = 1
ORDER BY trips.start_date;


-- 5. Находится ли сотрудник в командировке на дату:
--    отбор по нескольким условиям + COUNT.
--    Результат 0 - на месте, больше 0 - в командировке.
--    В приложении: employee_id = ? и сегодняшняя дата через ?
SELECT
    COUNT(*) AS active_trips
FROM trips
WHERE employee_id = 2
    AND is_cancelled = 0
    AND start_date <= '2026-11-03'
    AND end_date >= '2026-11-03';


-- 6. Сотрудники, свободные на выбранную дату (подзапрос NOT IN).
--    Внутренний запрос находит занятых сотрудников: у них есть
--    неотменённая командировка, в период которой входит дата.
--    В приложении дата передаётся параметром ? (дважды).
SELECT
    employees.id,
    employees.name,
    employees.position
FROM employees
WHERE employees.id NOT IN (
    SELECT trips.employee_id
    FROM trips
    WHERE trips.is_cancelled = 0
        AND trips.start_date <= '2026-11-03'
        AND trips.end_date >= '2026-11-03'
)
ORDER BY employees.name;


-- 7. Список командировок с сотрудником и маршрутом
--    (соединение трёх таблиц JOIN)
SELECT
    trips.id,
    trips.start_date,
    trips.end_date,
    trips.is_cancelled,
    employees.name AS employee_name,
    routes.origin,
    routes.destination
FROM trips
JOIN employees ON trips.employee_id = employees.id
JOIN routes ON trips.route_id = routes.id
ORDER BY trips.start_date;


-- 8. Командировки по признаку отмены (фильтрация по состоянию):
--    0 - активные, 1 - отменённые.
--    В приложении: WHERE trips.is_cancelled = ?
SELECT
    trips.id,
    trips.start_date,
    trips.end_date,
    trips.is_cancelled,
    employees.name AS employee_name,
    routes.origin,
    routes.destination
FROM trips
JOIN employees ON trips.employee_id = employees.id
JOIN routes ON trips.route_id = routes.id
WHERE trips.is_cancelled = 0
ORDER BY trips.start_date;


-- 9. Полная карточка командировки (JOIN + WHERE).
--    Продолжительность считается функцией julianday(),
--    сверка расходов с бюджетом - выражением CASE
--    (та же логика, что в Trip.duration() и check_budget_status()).
--    В приложении: WHERE trips.id = ?
SELECT
    trips.id,
    trips.start_date,
    trips.end_date,
    CAST(julianday(trips.end_date) - julianday(trips.start_date)
        AS INTEGER) AS duration_days,
    trips.budget_limit,
    trips.expenses,
    trips.is_cancelled,
    CASE
        WHEN trips.expenses IS NULL THEN 'Расходы ещё не внесены'
        WHEN trips.expenses > trips.budget_limit THEN 'Бюджет превышен'
        WHEN trips.expenses = trips.budget_limit
            THEN 'Бюджет использован полностью'
        ELSE 'Расходы в пределах бюджета'
    END AS budget_status,
    employees.id AS employee_id,
    employees.name AS employee_name,
    employees.position AS employee_position,
    routes.origin,
    routes.destination,
    routes.transport
FROM trips
JOIN employees ON trips.employee_id = employees.id
JOIN routes ON trips.route_id = routes.id
WHERE trips.id = 1;


-- 10. Общая статистика по командировкам
--     (агрегатные функции COUNT, SUM, AVG).
--     SUM(expenses) и AVG пропускают значения NULL.
SELECT
    COUNT(*) AS total_trips,
    SUM(CASE WHEN is_cancelled = 0 THEN 1 ELSE 0 END) AS active_trips,
    SUM(is_cancelled) AS cancelled_trips,
    SUM(expenses) AS total_expenses,
    AVG(budget_limit) AS avg_budget
FROM trips;


-- 11. Количество командировок и расходы по каждому сотруднику
--     (LEFT JOIN + GROUP BY). Отменённые не учитываются;
--     сотрудник без командировок остаётся в списке со значением 0.
SELECT
    employees.name AS employee_name,
    COUNT(trips.id) AS trips_count,
    COALESCE(SUM(trips.expenses), 0) AS total_expenses
FROM employees
LEFT JOIN trips
    ON employees.id = trips.employee_id
    AND trips.is_cancelled = 0
GROUP BY employees.id, employees.name
ORDER BY trips_count DESC, employees.name;


-- 12. Популярность маршрутов: число активных командировок
--     по каждому маршруту (LEFT JOIN + GROUP BY)
SELECT
    routes.origin,
    routes.destination,
    routes.transport,
    COUNT(trips.id) AS trips_count
FROM routes
LEFT JOIN trips
    ON routes.id = trips.route_id
    AND trips.is_cancelled = 0
GROUP BY routes.id, routes.origin, routes.destination, routes.transport
ORDER BY trips_count DESC, routes.destination;


-- 13. Сотрудники, у которых активных командировок больше заданного
--     числа (фильтрация групп HAVING).
--     WHERE отбирает строки до группировки, HAVING - группы после.
--     В приложении: HAVING COUNT(trips.id) > ?
SELECT
    employees.name AS employee_name,
    COUNT(trips.id) AS trips_count
FROM employees
JOIN trips ON employees.id = trips.employee_id
WHERE trips.is_cancelled = 0
GROUP BY employees.id, employees.name
HAVING COUNT(trips.id) > 1
ORDER BY trips_count DESC;


-- 14. Командировки с превышением бюджета
--     (WHERE со сравнением двух столбцов + JOIN)
SELECT
    trips.id,
    employees.name AS employee_name,
    routes.destination,
    trips.budget_limit,
    trips.expenses,
    trips.expenses - trips.budget_limit AS overrun
FROM trips
JOIN employees ON trips.employee_id = employees.id
JOIN routes ON trips.route_id = routes.id
WHERE trips.is_cancelled = 0
    AND trips.expenses > trips.budget_limit
ORDER BY overrun DESC;
