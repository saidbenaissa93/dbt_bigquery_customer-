{{ config(materialized='table') }}
with source_stg as (

    select * 
    from {{ ref('stg_retail_sales') }}

),

cleaned_sales as (

    select
        -- Nettoyage de la catégorie : supprime les espaces en trop et formate en Majuscule/Minuscules (ex: Electronics)
        trim(initcap(product_category)) as product_category,
        customer_segment,
        sales_amount,
        profit,
        quantity
    from source_stg

),

final as (

    select
        product_category,
        customer_segment,
        sum(sales_amount) as total_sales,
        sum(profit) as total_profit,
        count(*) as total_transactions,
        sum(quantity) as total_quantity_sold
    from cleaned_sales
    group by 1, 2

)

select * from final