# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
import psutil


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    database_size = fields.Char(string="Database Size", compute="_get_db_size")

    cpu_usage = fields.Char(string="Uso de CPU", compute="get_memory_usage")
    cpu_count = fields.Char(string="Cantidad de CPUs", compute="get_memory_usage")
    mem_total = fields.Char(string="Memoria total", compute="get_memory_usage")
    mem_used = fields.Char(string="Memoria utilizada", compute="get_memory_usage")
    mem_used_percent = fields.Char(string="Memoria utilizada %", compute="get_memory_usage")
    mem_free = fields.Char(string="Memoria libre", compute="get_memory_usage")
    disk_mem_total = fields.Char(string="Memoria total del disco", compute="get_memory_usage")
    disk_mem_used = fields.Char(string="Memoria de disco utilizada", compute="get_memory_usage")
    disk_mem_used_percent = fields.Char(string="Memoria de disco utilizada %", compute="get_memory_usage")
    disk_mem_free = fields.Char(string="Memoria de disco libre", compute="get_memory_usage")   
    mem_attachment = fields.Char(string="Memoria utilizada en documentos", compute="get_memory_usage")

    def get_memory_usage(self):
        self.cpu_usage = f'{psutil.cpu_percent()} %'
        self.cpu_count = psutil.cpu_count()
        attachments = self.env['ir.attachment'].sudo().search([])

        mem_info = psutil.virtual_memory()
        self.mem_total = f'{(mem_info.total/(1024*1024)):.0f} Mb'
        self.mem_used = f'{(mem_info.used/(1024*1024)):.0f} Mb'
        self.mem_used_percent = f'{mem_info.percent} %'
        self.mem_free = f'{(mem_info.free/(1024*1024)):.0f} Mb'

        disk_mem_info = psutil.disk_usage('/')
        self.disk_mem_total = f'{(disk_mem_info.total / (1024 * 1024)):.0f} Mb'
        self.disk_mem_used = f'{(disk_mem_info.used / (1024 * 1024)):.0f} Mb'
        self.disk_mem_used_percent = f'{disk_mem_info.percent} %'
        self.disk_mem_free = f'{(disk_mem_info.free / (1024 * 1024)):.0f} Mb' 
        # attachment size
        self.mem_attachment = f'{(sum(attachments.mapped("file_size")) / 1000000):.0f} Mb'

    @api.depends('name', 'partner_id')
    def _get_db_size(self):
        db_name = self._cr.dbname
        # pg_database_size: return size in bytes
        # pg_size_pretty: return size in human-readable form (UNITS)
        self._cr.execute('''
            SELECT pg_size_pretty(pg_database_size(db.datname)) 
            FROM pg_database AS db 
            WHERE datname = %s ''', (db_name,))
        db_size = self._cr.fetchone()
        self.database_size = db_size[0]

    def get_table_size(self):
        self._cr.execute('''
            SELECT row_number() over (ORDER BY pg_total_relation_size (c.oid)) as serial_no, c.relname , pg_size_pretty(pg_total_relation_size(c.oid)), c.relnamespace
            FROM pg_class AS c
            LEFT JOIN pg_namespace n ON (n.oid = c.relnamespace)
            WHERE nspname NOT IN %s AND c.relkind <> %s AND nspname !~ %s
            ORDER BY pg_total_relation_size (c.oid) DESC''', ([('pg_catalog','information_schema'),'i','^pg_toast']))
        size_of_table = self._cr.fetchall()
        relation_model = self.env['relation.table.size'].sudo().search([])
        if len(relation_model):
            self._cr.execute('TRUNCATE TABLE relation_table_size')
        for rec in size_of_table:
            self.env['relation.table.size'].sudo().create({
                'name': rec[1],
                'size': rec[2]
            })
        view_id = self.env.ref('db_size.relation_table_size_tree').id,
        return {
            'name': ('Table Size'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'views': [[view_id, 'list']],
            'res_model': 'relation.table.size',
            'target': 'current',
        }


class EachTableSize(models.Model):
    _name = 'relation.table.size'
    _description = "Get Size of each table of currect db"


    name = fields.Char(string="Table Name")
    size = fields.Char(string="Size")


