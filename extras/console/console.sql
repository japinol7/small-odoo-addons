-- Count invoices
select count(*) from account_move where id > 0;

-- List some sale orders
select id, name, partner_id, date_order, amount_total from sale_order where id in (4, 7);
select * from sale_order where id in (4, 7);

-- List some invoices
select * from account_move where id in (2, 3);

-- Set module to upgrade next time Odoo starts
update ir_module_module set state = 'to upgrade' where name in ('jap_sale');

-- List contacts emails from all companies which email is not null
select rp.id, rp.name, rp.email, company_id, rc.name as company, rp.active
    from res_partner rp
    inner join res_company rc on rp.company_id = rc.id
    where rp.email is not null
    ;
--
