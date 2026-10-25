-- ==========================================================
-- Сервис планирования командировок: структура базы данных
-- ==========================================================
-- Сущности предметной области:
--   employees - сотрудники;
--   routes    - маршруты;
--   trips     - командировки (связывают сотрудника и маршрут).
--
-- Связи:
--   trips.employee_id -> employees.id (у сотрудника много командировок)
--   trips.route_id    -> routes.id    (по маршруту много командировок)
--
-- IF NOT EXISTS позволяет выполнять скрипт повторно без ошибок.

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    transport TEXT NOT NULL
);

-- Даты хранятся строкой в формате YYYY-MM-DD: такие строки
-- сравниваются и сортируются как даты.
-- expenses может быть NULL - расходы ещё не внесены.
-- is_cancelled: 0 - командировка активна, 1 - отменена.
CREATE TABLE IF NOT EXISTS trips (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    route_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    budget_limit REAL NOT NULL,
    expenses REAL,
    is_cancelled INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (route_id) REFERENCES routes(id)
);
