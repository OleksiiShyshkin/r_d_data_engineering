/*
 Завдання на SQL до лекції 03.
 */


/*
1.
Вивести кількість фільмів в кожній категорії.
Результат відсортувати за спаданням.
*/

select
	c.name as film_category,
	count(distinct f.film_id) as film_count
from film f
inner join film_category fc on f.film_id = fc.film_id 
inner join category c on fc.category_id = c.category_id 
group by c.name
order by film_count desc;

/*
2.
Вивести 10 акторів, чиї фільми брали на прокат найбільше.
Результат відсортувати за спаданням.
*/

select
	a.actor_id,
	concat(a.first_name, ' ', a.last_name) as actor_name,
	count(distinct r.rental_id) as rental_count
from actor a 
inner join film_actor fa on a.actor_id  = fa.actor_id 
inner join film f on fa.film_id  = f.film_id 
inner join inventory i on i.film_id = f.film_id 
inner join rental r on r.inventory_id = i.inventory_id
group by a.actor_id, a.first_name, a.last_name
order by rental_count desc
limit 10;

/*
3.
Вивести категорію фільмів, на яку було витрачено найбільше грошей
в прокаті
 */

select 
	c.name as film_category,
	sum(p.amount) as total_sales
from payment p
inner join rental r on p.rental_id = r.rental_id
inner join inventory i on r.inventory_id = i.inventory_id
inner join film f on i.film_id = f.film_id
inner join film_category fc on f.film_id = fc.film_id
inner join category c on fc.category_id = c.category_id
group by c.name
order by total_sales desc
limit 1;

/*
4.
Вивести назви фільмів, яких не має в inventory.
Запит має бути без оператора IN
*/

select
	f.title
from film as f
left join inventory as i on f.film_id = i.film_id
where i.inventory_id is null;

/*
5.
Вивести топ 3 актори, які найбільше зʼявлялись в категорії фільмів “Children”.
*/

select
	a.actor_id,
	concat(a.first_name, ' ', a.last_name) as actor_name,
	count(distinct f.film_id) as film_count
from actor a 
inner join film_actor fa on a.actor_id  = fa.actor_id 
inner join film f on fa.film_id  = f.film_id 
inner join film_category fc on f.film_id = fc.film_id
inner join category c on fc.category_id = c.category_id
where c.name = 'Children'
group by a.actor_id, a.first_name, a.last_name
order by film_count desc
limit 3;
