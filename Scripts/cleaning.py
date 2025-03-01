from utils import get_db_connection

def remove_nulls_and_add_cascade():
    """Remove rows from tables where critical fields are NULL and add CASCADE to foreign key constraints."""
    
    # Establish connection to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Add ON DELETE CASCADE to the foreign key constraints
        cursor.execute("""
            ALTER TABLE tasks
            DROP CONSTRAINT IF EXISTS tasks_rep_id_fkey,
            ADD CONSTRAINT tasks_rep_id_fkey FOREIGN KEY (rep_id) REFERENCES sales_rep(rep_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE tasks
            DROP CONSTRAINT IF EXISTS tasks_customer_id_fkey,
            ADD CONSTRAINT tasks_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE interactions
            DROP CONSTRAINT IF EXISTS interactions_rep_id_fkey,
            ADD CONSTRAINT interactions_rep_id_fkey FOREIGN KEY (rep_id) REFERENCES sales_rep(rep_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE interactions
            DROP CONSTRAINT IF EXISTS interactions_customer_id_fkey,
            ADD CONSTRAINT interactions_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE interactions
            DROP CONSTRAINT IF EXISTS interactions_follow_up_task_id_fkey,
            ADD CONSTRAINT interactions_follow_up_task_id_fkey FOREIGN KEY (follow_up_task_id) REFERENCES tasks(task_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE opportunities
            DROP CONSTRAINT IF EXISTS opportunities_customer_id_fkey,
            ADD CONSTRAINT opportunities_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE opportunities
            DROP CONSTRAINT IF EXISTS opportunities_product_id_fkey,
            ADD CONSTRAINT opportunities_product_id_fkey FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE opportunities
            DROP CONSTRAINT IF EXISTS opportunities_rep_id_fkey,
            ADD CONSTRAINT opportunities_rep_id_fkey FOREIGN KEY (rep_id) REFERENCES sales_rep(rep_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE payments
            DROP CONSTRAINT IF EXISTS payments_customer_id_fkey,
            ADD CONSTRAINT payments_customer_id_fkey FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE user_sales_rep
            DROP CONSTRAINT IF EXISTS user_sales_rep_rep_id_fkey,
            ADD CONSTRAINT user_sales_rep_rep_id_fkey FOREIGN KEY (rep_id) REFERENCES sales_rep(rep_id) ON DELETE CASCADE;
        """)
        conn.commit()

        cursor.execute("""
            ALTER TABLE user_sales_rep
            DROP CONSTRAINT IF EXISTS user_sales_rep_user_id_fkey,
            ADD CONSTRAINT user_sales_rep_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;
        """)
        conn.commit()

        # Now, delete rows with NULL values in critical fields
        cursor.execute("""
            DELETE FROM users WHERE username IS NULL OR password_hash IS NULL OR email IS NULL OR role IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM customers WHERE name IS NULL OR email IS NULL OR phone IS NULL OR industry IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM sales_rep WHERE full_name IS NULL OR email IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM products WHERE name IS NULL OR description IS NULL OR price IS NULL OR stock_quantity IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM tasks WHERE customer_id IS NULL OR rep_id IS NULL OR task_type IS NULL OR due_date IS NULL OR status IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM opportunities WHERE customer_id IS NULL OR product_id IS NULL OR rep_id IS NULL OR status IS NULL OR estimated_value IS NULL OR close_date IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM payments WHERE customer_id IS NULL OR amount IS NULL OR payment_method IS NULL OR status IS NULL;
        """)
        conn.commit()

        cursor.execute("""
            DELETE FROM interactions WHERE customer_id IS NULL OR rep_id IS NULL OR interaction_type IS NULL OR interaction_date IS NULL;
        """)
        conn.commit()

    except Exception as e:
        print(f"Error altering constraints or deleting rows: {e}")

    finally:
        # Close database connection
        cursor.close()
        conn.close()

# Run the function to add CASCADE constraints and remove invalid rows
remove_nulls_and_add_cascade()
